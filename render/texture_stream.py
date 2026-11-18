"""第 51 批：开放世界骑乘坐骑穿城时，贴图一会儿糊一会儿爆内存...

修复点：
- feedback_delay: mip 反馈缓冲晚两帧 —— 量化反馈相对请求的延迟帧数，供补偿逻辑使用
- priority: 请求优先级按屏幕占比（并考虑距离与纹素密度），不再只看距离
- byte_budget: 预算按字节而非张数
- lock_page: 淘汰前检查正在采样的页是否被锁定
- fallback_mip: 缺页时回退到更低的 mip，而不是最高 mip
- dedupe_billing: 图集页与独立纹理页取并集，避免重复计费
- format_budget: sRGB 与线性纹理分开预算
"""


def feedback_delay(request_frame, sample_frame):
    """返回 mip 反馈相对请求的延迟帧数（反馈晚到为正，不晚则为 0）。"""
    return max(0, request_frame - sample_frame)


def priority(screen_coverage, distance, texel_density):
    """计算纹理请求优先级：屏幕占比越高、距离越近、纹素密度越大，优先级越高。"""
    if screen_coverage <= 0.0:
        return 0.0
    return screen_coverage * texel_density / (1.0 + max(0.0, distance))


def byte_budget(sizes, budget):
    """按字节预算返回可加载项索引（按给定顺序装入，直到预算耗尽）。"""
    chosen = []
    used = 0
    for i, size in enumerate(sizes):
        if used + size > budget:
            continue
        chosen.append(i)
        used += size
    return chosen


def lock_page(page_id, active_locks):
    """判断页是否被采样锁定（锁定的页禁止淘汰）。"""
    return page_id in active_locks


def fallback_mip(requested, available):
    """缺页时选择可用 mip：请求的 mip 不可用时回退到更低 mip，而不是最高 mip。"""
    if requested < available:
        return requested
    return max(0, available - 1)


def dedupe_billing(atlas_pages, standalone_pages):
    """合并图集页与独立纹理的计费集合（同一页只计一次）。"""
    return set(atlas_pages) | set(standalone_pages)


_FORMAT_SHARES = {
    "srgb": 0.6,
    "linear": 0.4,
}


def format_budget(format_name, total):
    """按纹理格式返回预算份额：sRGB 与线性纹理各自独立核算。"""
    return total * _FORMAT_SHARES.get(format_name, 0.5)
