# pairwise-texture-stream

开放世界骑乘坐骑穿城时，贴图一会儿糊一会儿爆内存：mip 反馈缓冲晚两帧；请求优先级只看距离不看屏幕占比；预算按张数不按字节；淘汰没锁正在采样页；缺页 fallback 用最高 mip；sRGB 和线性纹理共用预算；图集页与独立纹理重复计费；异步上传没做帧预算；虚拟纹理页表更新与采样竞争；跨区传送没重置流送器。render/texture_stream.py 是核心，tests/test_texture_stream.py 15个红。要修的是：反馈延迟补偿；按屏幕占比优先级；字节预算；采样页锁定；缺页低 mip fallback；按格式分预算；图集去重计费；上传帧预算；页表双缓冲；传送重置。

## 运行

```bash
python -m pytest tests -q
```

初始状态：15 个用例失败。修复实现使全部用例通过，不要修改 `tests/` 下的测试。

子方向：图形渲染；任务类型：Bugfix；语言/框架：Python 3, pytest；环境可复现等级：无外部依赖。
