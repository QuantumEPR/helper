# Blender COLMAP模型导入/导出插件

该插件允许您在Blender中导入和导出COLMAP模型。您可以轻松地将COLMAP相机和图像数据加载到Blender中，并将选定的对象导出回COLMAP格式。

## 安装

1. 下载此仓库的ZIP文件。
2. 打开Blender。
3. 转到 `编辑 > 首选项 > 插件`。
4. 在右上角的下拉菜单中，点击 `从磁盘安装`。
5. 选择您下载的ZIP文件。
6. 确保插件已启用，勾选插件列表中的复选框。

**注意：** 如果遇到与导入相关的错误，请确保Blender的Python（位于Blender安装目录下的Python）已安装`numpy`模块。

## 使用方法

### 导入COLMAP模型
导入COLMAP模型（相机和图像）：

1. 转到 `文件 > 导入 > COLMAP模型 (.bin)`。
2. 选择包含COLMAP模型数据的 `.bin` 文件。
3. 相机和图像将被导入到Blender场景中。

### 导出COLMAP模型
导出COLMAP模型（仅导出选中的对象）：

1. 在3D视图中选择您想要导出的对象。
2. 转到 `文件 > 导出 > COLMAP模型 (.bin)`。
3. 选择保存 `.bin` 文件的路径，文件将包含所选对象。

## 系统要求

- Blender（已在4.3上测试）
- Python `numpy` 模块（确保它已安装在Blender的Python环境中）

## 许可证

本项目采用MIT许可证 - 详情请参见 [LICENSE](LICENSE) 文件。
