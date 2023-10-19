import os
import regex as re

# 定义要查找和替换的模式
SWAGGER_PATTERN = r'@ApiModel\((.*?)\)\s*@ApiModelProperty\((.*?)\)'
OPENAPI_PATTERN = r'@Schema\((.*?)\)\s*@io\.swagger\.v3\.oas\.annotations\.Parameter\((.*?)\)'
SWAGGER_TAG_PATTERN = r'@Api(tags = "(.*?)")'
OPENAPI_TAG_PATTERN = r'@Tag(name = "(.*?)")'
SWAGGER_IMPLICIT_PARAMS_PATTERN = r'@ApiImplicitParams\((.*?)\)\s*'
OPENAPI_IMPLICIT_PARAMS_PATTERN = r'@io.swagger.v3.oas.annotations.parameters.ApiImplicitParams\((.*?)\)\s*'
SWAGGER_IMPLICIT_PARAM_PATTERN = r'@ApiImplicitParam\((.*?)\)\s*'
OPENAPI_IMPLICIT_PARAM_PATTERN = r'@io.swagger.v3.oas.annotations.parameters.ApiImplicitParam\((.*?)\)\s*'

# 定义要转换的依赖包
SWAGGER_DEPENDENCIES = [
    'io.swagger:swagger-annotations:1.5.0',
    'io.swagger:swagger-models:1.5.0',
    'io.swagger:swagger-core:1.5.0'
]
OPENAPI_DEPENDENCIES = [
    'io.swagger.core.v3:swagger-annotations:2.1.10',
    'io.swagger.core.v3:swagger-models:2.1.10',
    'io.swagger.core.v3:swagger-core:2.1.10'
]

# 定义要转换的目录和文件类型
DIRECTORY = '/Users/kenneth/Kenneth/Codes/2-invest-SpringBoot-SDK/spring-cloud-investoday-test/src/main/java/com/investoday/boot/controller'
FILE_TYPE = '.java'

# 遍历目录下的所有文件
for root, dirs, files in os.walk(DIRECTORY):
    for file in files:
        if file.endswith(FILE_TYPE):
            # 读取文件内容
            file_path = os.path.join(root, file)
            with open(file_path, 'r') as f:
                content = f.read()

            # 查找并替换注解
            content = re.sub(SWAGGER_PATTERN, OPENAPI_PATTERN, content)
            content = re.sub(SWAGGER_TAG_PATTERN, OPENAPI_TAG_PATTERN, content)
            content = re.sub(SWAGGER_IMPLICIT_PARAMS_PATTERN, OPENAPI_IMPLICIT_PARAMS_PATTERN, content)
            content = re.sub(SWAGGER_IMPLICIT_PARAM_PATTERN, OPENAPI_IMPLICIT_PARAM_PATTERN, content)

            # 查找并替换依赖包
            for i, dependency in enumerate(SWAGGER_DEPENDENCIES):
                content = content.replace(dependency, OPENAPI_DEPENDENCIES[i])

            # 查找并替换包名
            content = content.replace('io.swagger.annotations', 'io.swagger.v3.oas.annotations')
            content = content.replace('io.swagger.models', 'io.swagger.v3.oas.models')

            # 写入文件
            with open(file_path, 'w') as f:
                f.write(content)