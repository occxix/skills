# Browser Extension

## 核心规则
- 先确认浏览器、Manifest 版本和权限范围。
- 区分 popup、background/service worker、content script 的职责。
- 只申请必要权限，优先最小化权限和消息通道。
- 涉及发布时，检查打包、资源注入和跨浏览器兼容性。

