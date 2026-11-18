"""第 51 批：开放世界骑乘坐骑穿城时，贴图一会儿糊一会儿爆内存..."""

def feedback_delay(request_frame, sample_frame):
    """返回 mip 反馈相对请求的延迟帧数。"""
    raise NotImplementedError("TODO: feedback_delay")

def priority(screen_coverage, distance, texel_density):
    """计算纹理请求优先级。"""
    raise NotImplementedError("TODO: priority")

def byte_budget(sizes, budget):
    """按字节预算返回可加载项索引。"""
    raise NotImplementedError("TODO: byte_budget")

def lock_page(page_id, active_locks):
    """判断页是否被采样锁定。"""
    raise NotImplementedError("TODO: lock_page")

def fallback_mip(requested, available):
    """缺页时选择可用 mip。"""
    raise NotImplementedError("TODO: fallback_mip")

def dedupe_billing(atlas_pages, standalone_pages):
    """合并图集页与独立纹理的计费集合。"""
    raise NotImplementedError("TODO: dedupe_billing")

def format_budget(format_name, total):
    """按纹理格式返回预算份额。"""
    raise NotImplementedError("TODO: format_budget")
