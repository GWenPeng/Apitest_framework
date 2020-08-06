/*********************************************************************************
ShareMgnt.thrift:
    管理功能的thrift接口定义文件
    Copyright (c) Eisoo Software, Inc.(2004 - 2013), All rights reserved.

Purpose:
    定义AnyShare管理控制台接口

Author:
    zhang.ying@eisoo.com
    yuan.chensi@eisoo.com
    zou.yongbo@eisoo.com
    li.guangyou@eisoo.com
    wei.xiaodong@eisoo.com
    ouyang.xu@eisoo.com
    zhang.bin@eisoo.com
    chu.chenggang@eisoo.com
    zhang.feng01@eisoo.com
    li.jiacheng@eisoo.com
    liu.yue@eisoo.com
    yang.qingshuai@eisoo.com
    chen.liang@eisoo.com
    wang.chunlu@eisoo.com

Creating Time:
    2013-07-03

简介：

一、ShareMgnt提供AnyShare管理控制台的Thrift接口，包括:
1. 组织管理
2. 部门管理
3. 用户管理
4. 权责分离管理
5. 第三方管理
6. 域控管理
7. 导入用户管理
8. 联系人管理
9. 在线用户统计管理
11. OEM管理
12. SMTP服务器管理
13. 告警管理
14. Nginx配置管理
15. 系统密级管理
16. 发现共享限制管理
17. 外链共享限制管理
18. 权限共享限制管理
19. 防泄密权限管理
20. 认证接口
21. 缓存配置管理
22. 登录策略管理
23. 客户端升级包管理
24. 多租户管理
25. 提供给 openapi 使用
26. 共享审核策略配置管理
27. 第三方预览工具管理
29. 用户登录访问控制管理
30. 文档审核流程控制
31. 处理集成到anyshare的外部应用
32. 涉密模块处理
33. 跨网段数据交换
34. NAS服务配置管理
35. 邀请共享管理
36. 限速管理
37. 第三方标密系统配置
38. 文件水印策略配置
39. 内外链共享模板策略
40. 网段文档库绑定管理
41. 文档下载限制管理
42. 共享文档配置管理
43. 文件留底配置管理
44. 权限共享屏蔽组织架构信息管理
46. 文件改密需要审核配置接口
47. 外链留底配置管理
48. 设备绑定查询
49. 防病毒管理
50. 导出日志文件管理
51. 回收站配置管理
52. 短信服务器配置管理
53. 删除文档库延迟天数配置
54. 活跃用户统计管理
55. 用户角色管理
56. 文件抓取配置管理
57. 个人文档自动归档策略管理
58. 个人文档自动清理策略管理
59. 指定文档库病毒扫描管理
60. 本地同步策略
61. 用户空间使用信息导出管理
62. webhook 管理
63. 快速入门管理

二、ShareMgnt提供的错误码说明：
ShareMgnt提供的错误码共5位，如10111。第一位表示错误级别，二三位表示模块类型，四五位表示具体错误信息。
模块状态码信息如下：
00：未知模块
01：用户和联系人
02：组织和部门
03：批量导入导出
04：域控
06：第三方
07：OEM配置管理
12: 审核策略管理
13: 第三方预览工具管理
14: 用户登录访问控制管理
*********************************************************************************/

include "EThriftException.thrift"
include "EACPLog.thrift"

// 端口号
const i32 NCT_SHAREMGNT_PORT = 9600

// admin,audit,security和system用户
const string NCT_USER_ADMIN = '266c6a42-6131-4d62-8f39-853e7093701c'
const string NCT_USER_AUDIT = '94752844-BDD0-4B9E-8927-1CA8D427E699'
const string NCT_USER_SYSTEM = '234562BE-88FF-4440-9BFF-447F139871A2'
const string NCT_USER_SECURIT = '4bb41612-a040-11e6-887d-005056920bea'

// 系统内置各角色id标识
const string NCT_SYSTEM_ROLE_SUPPER = '7dcfcc9c-ad02-11e8-aa06-000c29358ad6'
const string NCT_SYSTEM_ROLE_ADMIN = 'd2bd2082-ad03-11e8-aa06-000c29358ad6'
const string NCT_SYSTEM_ROLE_SECURIT = 'd8998f72-ad03-11e8-aa06-000c29358ad6'
const string NCT_SYSTEM_ROLE_AUDIT = 'def246f2-ad03-11e8-aa06-000c29358ad6'
const string NCT_SYSTEM_ROLE_ORG_MANAGER = 'e63e1c88-ad03-11e8-aa06-000c29358ad6'
const string NCT_SYSTEM_ROLE_ORG_AUDIT = 'f06ac18e-ad03-11e8-aa06-000c29358ad6'
const string NCT_SYSTEM_ROLE_SHARED_APPROVE = 'f58622b2-ad03-11e8-aa06-000c29358ad6'
const string NCT_SYSTEM_ROLE_DOC_APPROVE = 'fb648fac-ad03-11e8-aa06-000c29358ad6'
const string NCT_SYSTEM_ROLE_CSF_APPROVE = '01a78ac2-ad04-11e8-aa06-000c29358ad6'


// 默认组织结构id
const string NCT_DEFAULT_ORGANIZATION = '151bcb65-48ce-4b62-973f-0bb6685f9cb8'

// 未分配用户组id
const string NCT_UNDISTRIBUTE_USER_GROUP = '-1'

// 所有用户组id
const string NCT_ALL_USER_GROUP = '-2'

// 用户直属部门
const string NCT_DIRECT_DEPARTMENT = '-3'

// 用户直属组织
const string NCT_DIRECT_ORGANIZATION = '-4'

// 定义内外网数据交换流程id
const string NCT_DOC_EXCHANGE_PROCESSID = '-1'

// 用户类型
enum ncTUsrmUserType {
    NCT_USER_TYPE_LOCAL = 1,        // 本地用户
    NCT_USER_TYPE_DOMAIN = 2,       // 域用户
    NCT_USER_TYPE_THIRD = 3,        // 第三方验证用户
}

// 用户状态
enum ncTUsrmUserStatus {
    NCT_STATUS_ENABLE = 0,          // 启用
    NCT_STATUS_DISABLE = 1,         // 禁用
    NCT_STATUS_DELETE = 2,          // 用户被第三方系统删除
}

// 部门类型
enum ncTUsrmDepartType {
    NCT_DEPART_TYPE_LOCAL = 1,      // 本地部门
    NCT_DEPART_TYPE_DOMAIN = 2,     // 域部门
    NCT_DEPART_TYPE_THIRD = 3,      // 第三方用户系统的部门
}

// 域控类型
enum ncTUsrmDomainType {
    NCT_DOMAIN_TYPE_PRIMARY = 1,    // 主域
    NCT_DOMAIN_TYPE_SUB = 2,        // 子域
    NCT_DOMAIN_TYPE_TRUST = 3,      // 信任域
}

// 数据库类型
enum ncTDBType {
    NCT_MYSQL = 1,              // Mysql数据库
    NCT_ORACLE = 2,             // Oracle数据库
    NCT_MSSQL = 3,              // MS SQL Server数据库
}

// 认证类型
enum ncTUsrmAuthenType {
    NCT_AUTHEN_TYPE_MANAGER     = 1,    // 管理员身份
    NCT_AUTHEN_TYPE_NORMAL      = 2,    // 普通用户身份
    NCT_AUTHEN_TYPE_THIRD       = 3,    // 第三方认证系统
}

// 最小机密等级
const i32 NCT_MIN_CSF_LEVEL = 5

// 归属站点信息
struct ncTUsrmSiteInfo {
    1: string id;                               // 站点ID
    2: string name;                             // 站点名
}

//对象存储信息
struct ncTUsrmOSSInfo {
    1: string ossId;                            // 对象存储ID
    2: string ossName;                          // 对象存储名称
    3: string siteName;                         // 对象存储归属站点名称
    4: bool enabled;                            // 对象存储状态
    5: i32 type,                                // 0 表示当前站点配置、管理的对象存储，1 表示分站点同步到总站点的对象存储
}

// 管理员限额信息
struct ncTLimitSpaceInfo {
    1: optional i64 limitUserSpace                 // 用户限额，默认为-1(无限制)
    2: optional i64 allocatedLimitUserSpace        // 已分配的用户限额,默认0
    3: optional i64 limitDocSpace                  // 文档库限额，默认为-1(无限制)
    4: optional i64 allocatedLimitDocSpace         // 已分配的文档库限额，默认0
}

// 用户角色信息
struct ncTRoleInfo
{
    1: string name;                 // 名称
    2: string description;          // 描述
    3: string creatorId;            // 创建者id
    4: string id;                   // 角色id标识
    5: string displayName;          // 显示名
}

// 管辖部门信息
struct ncTManageDeptInfo {
    1: list<string> departmentIds;                 // 所属部门id，-1时表示为未分配用户
    2: list<string> departmentNames;               // 所属部门名称
    3: i64 limitUserSpaceSize;                     // 用户限额
    4: i64 limitDocSpaceSize;                      // 文档库限额
}

// 审核类型
enum ncTAuditType
{
    NCT_PERM_SHARE = 1,                            // 共享审核员类型，包括内链、外链、所有者权限审核
    NCT_CSF_LEVEL = 2,                             // 密级审核员类型
    NCT_PERM_AND_CSF_SHARE = 3,                    // 共享及密级审核员类型
    NCT_DOC_FLOW = 4,                              // 文档流程审核员类型
}


// 审核员审核对象类型
enum ncTAuditObjectType
{
    NCT_AUDIT_OBJECT_USER = 1,              // 用户
    NCT_AUDIT_OBJECT_DEPT = 2,              // 部门
    NCT_AUDIT_OBJECT_LIBRARY = 3,           // 文档库
    NCT_AUDIT_OBJECT_ARCHIVE = 4,           // 归档库
}

// 审核员审核对象
struct ncTAuditObject
{
     1: ncTAuditObjectType       objType;
     2: string                   objId;
     3: string                   objName;
}

// 角色成员信息
struct ncTRoleMemberInfo {
    1: string userId;                              // 用户id
    2: string displayName;                         // 显示名
    3: list<string> departmentIds;                 // 所属部门id，-1时表示为未分配用户
    4: list<string> departmentNames;               // 所属部门名称
    5: ncTManageDeptInfo       manageDeptInfo;     // 管辖部门信息
    6: list<ncTAuditObject>    auditObj;           // 审核对象
}

// 用户基本信息
struct ncTUsrmUserInfo {
    1: required string loginName;                   // 用户名称
    2: optional string displayName;                 // 显示名
    3: optional string email;                       // 邮箱
    4: optional i64 space;                          // 配额空间，单位Bytes，默认5GB，最小1GB
    5: optional ncTUsrmUserType userType;           // 用户类型
    6: required list<string> departmentIds;         // 所属部门id，-1时表示为未分配用户
    7: optional list<string> departmentNames;       // 所属部门名称
    8: optional ncTUsrmUserStatus status;           // 用户状态
    9: optional i64 usedSize;                       // 已使用配额空间,单位Bytes
    10: optional i32 priority;                      // 排序优先级
    11: optional i32 csfLevel;                      // 用户密级
    12: required bool pwdControl;                   // 密码管控
    13: optional ncTUsrmOSSInfo ossInfo;             // 对象存储信息
    14: optional ncTLimitSpaceInfo limitSpaceInfo;  // 管理员限额信息
    15: optional i64 createTime;                    // 用户创建时间
    16: optional bool freezeStatus;                 // 用户冻结状态，true:冻结 false:未冻结
    17: optional string telNumber;                  // 手机号
    18: optional list<ncTRoleInfo> roles;           // 用户角色
    19: optional i32 expireTime;                    // 用户账号有效期(单位：秒), 默认为 -1, 永久有效
    20: optional string remark;                     // 备注
    21: optional string idcardNumber;               // 身份证号
}

// 定义简单的用户信息
struct ncTSimpleUserInfo {
    1: string id;
    2: string displayName;
    3: string loginName;
    4: ncTUsrmUserStatus status;
}

// 直属部门信息
struct ncTUsrmDirectDeptInfo {
    1: string departmentId;                                     // 部门id
    2: string departmentName;                                   // 部门名称
    3: list<ncTSimpleUserInfo> responsiblePersons;              // 管理员信息
}

// 用户节点信息
struct ncTUsrmGetUserInfo {
    1: required string id;                      // 用户id
    2: ncTUsrmUserInfo user;                    // 用户基本信息
    3: optional bool originalPwd;               // 是否为初始密码
    4: optional string password;                // 用户密码
    5: ncTUsrmDirectDeptInfo directDeptInfo;    // 直属部门信息
}

// 密码强度和时效性信息，某个参数变量如果为None,则后台不做处理
// 如果不需更改某个密码配置参数，则设置为None
struct ncTUsrmPasswordConfig {
    1: required bool strongStatus;      // 强密码状态
    2: required i32 expireTime;         // 密码有效期(单位:天), -1: 永不失效
    3: required bool lockStatus;        // 锁定状态
    4: required i32 passwdErrCnt;       // 密码错误次数
    5: optional i32 passwdLockTime;     // 密码锁定时间(以分钟为单位)
    6: required i32 strongPwdLength;    // 强密码的最小长度
}

// 新建用户时的信息
struct ncTUsrmAddUserInfo {
    1: ncTUsrmUserInfo user;            // 用户基本信息
    2: required string password;         // 密码，此处为明文
}

// 修改用户参数
struct ncTEditUserParam {
    1: required string id;              // 用户id
    2: optional string displayName;     // 显示名称
    3: optional string email;           // 邮箱名称
    4: optional i64 space;              // 配额空间
    5: optional i32 priority;           // 权重排序
    6: optional i32 csfLevel;           // 密级
    7: optional bool pwdControl;        // 密码管控
    8: optional string pwd;             // 密码
    9: optional string ossId;           // 用户配置对象存储ID，可以为空
    10: optional string telNumber;      // 手机号
    11: optional i32 expireTime;        // 用户账号有效期(单位：秒), 默认为 -1, 永久有效
    12: optional string remark;         // 备注
    13: optional string idcardNumber;   // 身份证号
}

// 新建组织操作参数
struct ncTAddOrgParam {
    1: required string orgName;                 // 组织名
    2: optional string ossId;                   // 组织配置对象存储ID，可以为空
    3: optional i32 priority;                   // 权重排序
    4: optional string email;                   // 组织邮箱地址
}

// 新建部门操作参数
struct ncTAddDepartParam {
    1: required string departName;              // 组织或部门名
    2: required string parentId;                // 父部门Id
    3: optional string ossId;                   // 组织配置对象存储ID，可以为空
    4: optional i32 priority;                   // 权重排序
    5: optional string email;                   // 部门邮箱地址
}

// 编辑组织或部门参数信息
struct ncTEditDepartParam {
    1: required string departId;                // 组织或部门ID
    2: optional string departName;              // 组织或部门名
    3: optional string ossId;                   // 组织配置对象存储ID，可以为空
    4: optional i32 priority;                   // 权重排序
    5: optional string email;                   // 组织或部门邮箱地址
}

// 部门信息
struct ncTUsrmDepartmentInfo {
    1: string departmentId;                                     // 部门id
    2: string departmentName;                                   // 部门名称
    3: string parentDepartId;                                   // 父部门id
    4: string parentDepartName;                                 // 父部门名称
    5: list<ncTUsrmGetUserInfo> responsiblePersons;             // 部门管理员
    6: ncTUsrmOSSInfo ossInfo;                                   // 对象存储信息
    7: optional list<string> subDepartIds;                      // 子部门id
    8: string email;                                            // 部门邮箱地址
    9: optional string parentPath;                              // 父部门路径
}

// 部门节点信息
struct ncTDepartmentInfo {
    1: string id;                                               // 部门id
    2: string name;                                             // 部门名称
    3: list<ncTUsrmGetUserInfo> responsiblePersons;             // 部门管理员
    4: i32 subDepartmentCount;                                  // 子部门数量
    5: i32 subUserCount;                                        // 子用户数量
    6: ncTUsrmOSSInfo ossInfo;                                   // 对象存储信息
    7: string email;                                            // 部门邮箱地址
}

// 组织信息
struct ncTUsrmOrganizationInfo {
    1: string organizationId;                                   // 组织id
    2: string organizationName;                                 // 组织名称
    3: list<ncTUsrmDepartmentInfo> departments;                 // 组织的部门
    4: list<ncTUsrmGetUserInfo> responsiblePersons;             // 组织管理员
    5: ncTUsrmOSSInfo ossInfo;                                   // 对象存储信息
    6: string email;                                            // 组织邮箱地址
}

// 组织节点信息
struct ncTRootOrgInfo {
    1: bool isOrganization;                                     // 是否是组织，true表示组织，false表示部门
    2: string id;                                               // id
    3: string name;                                             // 名称
    4: list<ncTUsrmGetUserInfo> responsiblePersons;             // 管理员
    5: i32 subDepartmentCount;                                  // 子部门数量
    6: i32 subUserCount;                                        // 子用户数量
    7: ncTUsrmOSSInfo ossInfo;                                   // 对象存储信息
    8: string email;                                            // 组织邮箱地址
}

// 搜索时返回的用户信息
struct ncTSearchUserInfo {
    1: string id;                           // 用户id
    2: string loginName;                    // 用户登录名
    3: string displayName;                  // 用户显示名
    4: i32 csfLevel;                        // 用户密级
    5: list<string> departmentIds;          // 所属部门id，-1时表示为未分配用户
    6: list<string> departmentNames;        // 所属部门名称
    7: list<string> departmentPaths;        // 所属部门路径
}

// 定位用户时，单级的部门信息
struct ncTLocateInfo {
    1: string departId;                     // 部门id
    2: string departName;                   // 部门名称
}

//域同步方式
enum ncTUsrmDomainSyncMode {
    NCT_SYNC_UPPER_OU = 0,                  //同步对象包括上层组织结构
    NCT_NOT_SYNC_UPPER_OU = 1,              //不同步上层组织结构
    NCT_SYNC_USERS_ONLY = 2,                //仅同步用户
}

//域配置信息
struct ncTUsrmDomainConfig {
    1: string destDepartId;                 //要导入到的目的组织或部门id
    2: string desetDepartName;              //设置域配置信息的时候，设为None
    3: list<string> ouPath;                 //要导入的域组织路径，空为导入整个域
    4: i64 syncInterval;                    //同步时间间隔
    5: i64 spaceSize;                       //用户配额空间
    6: ncTUsrmDomainSyncMode syncMode;      //同步方式
    7: bool userEnableStatus;               //用户默认创建状态，true:启用 false:禁用
    8: bool forcedSync;                     //强制同步方式
    9: i32 validPeriod;                     //用户账号有效期(单位：天), 默认为 -1, 永久有效
}

//域关键字属性配置
struct ncTUsrmDomainKeyConfig {
    1: list<string> departNameKeys;               //部门名对应的域key字段
    2: list<string> departThirdIdKeys;            //部门ID对应的域key字段
    3: list<string> loginNameKeys;                //登录名对应的域key字段
    4: list<string> displayNameKeys;              //显示名对应的域key字段
    5: list<string> emailKeys;                    //用户邮箱对应的域key字段
    6: list<string> userThirdIdKeys;              //用户Id对应的域key字段
    7: list<string> groupKeys;                    //安全组信息的key字段
    8: string subOuFilter;                        //搜索子部门的Filter
    9: string subUserFilter;                      //搜索子用户的Filter
    10: string baseFilter;                        //具体某个部门或用户信息的filter
    11: list<string> statusKeys;                  //用户状态对应的域key字段
    12: list<string> idcardNumberKeys;            //用户身份证号对应的域key字段
}

// 备用域控信息
struct ncTUsrmFailoverDomainInfo {
    1: required i64 id;                         // 备用域id
    2: required i64 parentId;                   // 首选域id
    3: required string address;                 // 域控制器地址
    4: required i64 port;                       // 域端口
    5: required string adminName;               // 管理员账号
    6: required string password;                // 管理员密码
    7: optional bool useSSL;                    // 是否使用ssl连接，true-使用，false-不使用,默认不启用
}

// 域控信息
struct ncTUsrmDomainInfo {
    1: required i64 id;                         // 域id
    2: required ncTUsrmDomainType type;         // 1：主域，2：子域，3：信任域
    3: required i64 parentId;                   // 主域时，为 -1，子域或者信任域时，为主域的id值
    4: required string name;                    // 域名
    5: required string ipAddress;                  // 域ip
    6: required i64 port;                       // 域端口
    7: required string adminName;               // 管理员账号
    8: required string password;                // 管理员密码
    9: required bool status;                    // 状态,true-启用，false-禁用
    10: i32 syncStatus;                         // 同步状态, -1 关闭, 0 正向同步, 1 反向同步
    11: ncTUsrmDomainConfig config;             //域配置信息
    12: optional bool useSSL;                  // 是否使用ssl连接，true-使用，false-不使用,默认不启用
}

// 域用户信息
struct ncTUsrmDomainUser {
    1: string loginName;        // 登录名
    2: string displayName;      // 显示名
    3: string email;            // 邮箱
    4: string ouPath;           // 所属部门的路径，格式：OU=研发部, DC=test2,DC=develop,DC=cn
    5: string objectGUID;       // 对象的GUID，具有唯一性
    6: string dnPath;           // dnPath
    7: string idcardNumber;     // 身份证号
}

// 域组织单位信息
struct ncTUsrmDomainOU {
    1: string name;             // 组织名称
    2: string rulerName;        // 组织负责人
    3: string pathName;         // 路径，格式：OU=研发部, DC=test2,DC=develop,DC=cn
    4: string parentOUPath;     // 父部门的路径，格式：OU=研发部, DC=test2,DC=develop,DC=cn
    5: string objectGUID;       // 对象的GUID，具有唯一性
    6: bool importAll;          // 是否导入组织下的所有子组织及用户，True--导入，False--只导入此组织
}

// 域节点信息
struct ncTUsrmDomainNode {
    1: list<ncTUsrmDomainOU> ous;           // 组织
    2: list<ncTUsrmDomainUser> users;       // 用户
}

// 域用户导入的配置选项
struct ncTUsrmImportOption {
    1: required bool userEmail;                 // 是否导入用户邮箱
    2: required bool userDisplayName;           // 是否导入用户显示名
    3: required bool userCover;                 // 是否覆盖已有用户
    4: required bool userIdcardNumber;          // 是否导入身份证号
    5: required string departmentId;            // 导入目的地
    6: i64 spaceSize;                           // 用户的配额空间
    7: required ncTUsrmUserStatus userStatus;   // 用户创建默认状态
    8: i32 expireTime;                          // 用户账号有效期(单位：秒), 默认为 -1, 永久有效
}

// 需要导入的内容
struct ncTUsrmImportContent {
    1: ncTUsrmDomainInfo domain;        // 选择导入目标所属的域控信息
    2: string domainName;               // 勾选的域控，当domainName不为None时，代表导入整个域用户，此时users和ous为None
    3: list <ncTUsrmDomainUser> users;  // 勾选的域用户
    4: list <ncTUsrmDomainOU> ous;      // 勾选的域组织
}

// 导入的结果
struct ncTUsrmImportResult {
    1: i64 totalNum;            // 需要导入的总数
    2: i64 successNum;          // 已导入的总数
    3: i64 failNum;             // 出错总数
    4: list<string> failInfos;  // 错误内容
    5: i64 disableNum;          // 因用户授权数不足被禁用的数量
}

// 批量导入、导出用户信息文件
struct ncTBatchUsersFile {
    1: string fileName;         // 文件名
    2: binary data;             // 文件类容
}

// 导入失败错误信息
struct ncTImportFailInfo {
    1: i64 index;                            // 错误的行数
    2: ncTUsrmUserInfo userInfo;             // 用户信息
    3: string errorMessage;                  // 错误信息
    4: i64 errorID;                          // 错误码
}

// 在线用户数信息
struct ncTOpermOnlineUserInfo {
    1: string time;         // 记录的时间，格式：“2012-11-22 00:00:00”
    2: i64 count;           // 在线用户数
}

// 联系人组
struct ncTPersonGroup {
    1: string groupId;
    2: string groupName;
    3: optional i64 personCount;
}

// 搜索联系人组信息
struct ncTSearchPersonGroup {
    1: string userId;                       // 用户id
    2: string loginName;                    // 用户登录名
    3: string displayName;                  // 用户显示名
    4: string groupId;                      // 群组id
    5: string groupName;                    // 群组名
}

// oem配置信息
struct ncTOEMInfo {
    1: string           section;
    2: string           option;
    3: binary           value;
}

// SMTP配置
struct ncTSmtpSrvConf {
    1: string server;                      //邮件服务器
    2: byte safeMode;                      //0：无 1：SSL/TLS 2:STARTTLS
    3: i32 port;                           //服务器端口   PS:就这个有默认值 25
    4: string email;                       //发送地址
    5: optional string password;           //密码
    6: bool openRelay;                     //openRelay  PS:默认值false(关闭)
}

// 告警配置
struct ncTAlarmConfig
{
    1: i32 infoConfig;             //信息等级  0:None  1:email
    2: i32 warnConfig;             //警告等级
    3: list<string> emailToList;   //邮件接收者列表
}

// EfspWeb节点设置端口结果
struct ncTSetPortResult {
    1: string           nodename;       // 节点名称
    2: bool             suc;            // 是否成功
    3: string           msg;            // 如果失败，则msg为失败原因
}

// 发现共享策略信息
struct ncTFindShareInfo
{
    1: i32    sharerType;                // 共享者类型 1:用户, 2:部门
    2: string sharerId;                  // 共享者id
    3: string sharerName;                // 共享者名
}

// 外链共享策略信息
struct ncTLinkShareInfo
{
    1: i32    sharerType;                // 共享者类型 1:用户, 2:部门
    2: string sharerId;                  // 共享者id
    3: string sharerName;                // 共享者名
}

// 权限共享范围限制的共享者和共享对象组合对象信息
struct ncTShareObjInfo
{
    1: string id;                            // 组对象id
    2: string name;                          // 组对象名
    3: optional string parentId;             // 父部门id
    4: optional string parentName;           // 父部门名
}

// 权限共享范围限制的策略信息
struct ncTPermShareInfo
{
    1: string strategyId;                       // 权限共享范围策略信息ID
    2: list<ncTShareObjInfo> sharerUsers;       // 共享者 用户列表
    3: list<ncTShareObjInfo> sharerDepts;       // 共享者 部门列表
    4: list<ncTShareObjInfo> scopeUsers;        // 共享范围 用户列表
    5: list<ncTShareObjInfo> scopeDepts;        // 共享范围 部门列表
    6: bool status;                             // 状态
}

// 添加防泄密策略参数
struct ncTAddLeakProofStrategyParam
{
    1: string accessorId;           // 访问者Id，可为用户id，或者部门id
    2: i32 accessorType;            // 访问者类型，1表示用户，2表示部门
    3: i32 permValue;               // 权限值，1表示打印，2表示拷屏，3表示打印/拷屏
}

// 编辑防泄密策略参数
struct ncTEditLeakProofStrategyParam
{
    1: i64 strategyId;              // 策略id，唯一标识一条策略
    2: optional i32 permValue;      // 权限值，1表示打印，2表示拷屏，3表示打印/拷屏
}

// 防泄密策略信息
struct ncTLeakProofStrategyInfo
{
    1: i64 strategyId;              // 策略id，唯一标识一条策略
    2: string accessorId;           // 访问者Id，可为用户id，或者部门id
    3: i32 accessorType;            // 访问者类型，1表示用户，2表示部门
    4: i32 permValue;               // 权限值，1表示打印，2表示拷屏，3表示打印/拷屏
    5: string accessorName;         // 访问者名称
}

// 防泄密策略信息
struct ncTEOSSPortInfo
{
    1: i32 httpPort;                // http端口
    2: i32 httpsPort;               // https端口
}

// 客户端升级包相关数据类型
enum ncTOSType {
    android = 2,
    mac = 3,
    WIN_32_ADVANCED = 4,
    WIN_64_ADVANCED = 5,
    officePlugin = 6,
    iOS = 7
}

// 客户端升级包信息
struct ncTClientPackageInfo {
    1: required ncTOSType ostype;
    2: required string name;
    3: required i64 size;
    4: required string version;
    5: required string time;
    6: required bool mode;
    7: string url;             // 升级包URL，上传到本地对象存储时该项返回值为空，独立配置升级包下载地址返回配置的URL
}

// nginx证书信息
struct ncTCertInfo {
    1:string issuer                     // 证书颁发者
    2:string accepter                   // 证书接受者
    3:string startDate                  // 有效期开始日期
    4:string expireDate                 // 有效期过期日期
    5:bool hasExpired                   // 是否过期
}

// 第三方数据同步信息
struct ncTThirdDBInfo {
    1: string id;                     // 唯一表示第三方数据库
    2: string name;                   // 自定义名称
    3: string ip;                     // 数据库ip
    4: string port;                   // 端口
    5: string admin;                  // 管理员账号
    6: string password;               // 密码
    7: string database;               // 数据库实例名
    8: string charset;                // 数据库编码
    9: ncTDBType dbType;              // 数据库类型
    10: bool status;                   // 数据同步状态
}

// 第三方部门表信息
struct ncTThirdDepartTableInfo {
    1: string thirdDbId;                              // 第三方数据库id
    2: string tableId;                                // 表ID
    3: string tableName;                              // 部门表名
    4: string departmentIdField;                      // 部门id的表字段
    5: string departmentNameField;                    // 部门名的表字段
    6: string departmentPriorityField;                // 部门优先级的表字段
    7: string filter;                                 // 部门过滤器
    8: list<string> customSubGroupNames;              // 自定义子组名
}

// 第三方部门关系表信息
struct ncTThirdDepartRelationTableInfo {
    1: string thirdDbId;                              // 第三方数据库id
    2: string tableId;                                // 表ID
    3: string tableName;                              // 部门关系表名
    4: string departmentIdField;                      // 部门id的表字段
    5: string parentDepartmentIdField;                // 父部门id的表字段
    6: string parentCustomGroupTableId;               // 自定义父分组的表id
    7: list<string> parentCustomGroupName;            // 自定义父分组的名
    8: string filter;                                 // 部门关系过滤器
}

// 第三方用户表信息
struct ncTThirdUserTableInfo {
    1: string thirdDbId;                              // 第三方数据库id
    2: string tableId;                                // 表ID
    3: string tableName;                              // 用户信息表名
    4: string userIdField;                            // 用户id的表字段
    5: string userLoginNameField;                     // 用户登录名的表字段
    6: string userDisplayNameField;                   // 用户显示名的表字段
    7: string userEmailField;                         // 用户邮箱的表字段
    8: string userPasswordField;                      // 用户密码的表字段
    9: string userStatusField;                        // 用户状态的表字段
    10: string userPriorityField;                     // 用户优先级的表字段
    11: string filter;                                // 用户过滤器
}

// 第三方用户关系表信息
struct ncTThirdUserDepartRelationTableInfo {
    1: string thirdDbId;                              // 第三方数据库id
    2: string tableId;                                // 表ID
    3: string tableName;                              // 用户部门关系表名
    4: string userIdField;                            // 用户id的表字段
    5: string parentDepartmentIdField;                // 父部门id的表字段
    6: string parentCustomGroupTableId;               // 自定义父分组的表id
    7: list<string> parentCustomGroupName;            // 自定义父分组的名
    8: string filter;                                 // 用户关系过滤器
}

// 第三方数据库表信息
struct ncTThirdTableInfo {
    1: list<ncTThirdDepartTableInfo> thirdDepartTableInfos;
    2: list<ncTThirdDepartRelationTableInfo> thirdDepartRelationTableInfos;
    3: list<ncTThirdUserTableInfo> thirdUserTableInfos;
    4: list<ncTThirdUserDepartRelationTableInfo> thirdUserRelationTableInfos;
}

// 第三方数据同步配置信息
struct ncTThirdDbSyncConfig {
    1: string parentDepartId;               // 要导入到的目的组织或部门id
    2: string thirdRootName;                // 自定义第三方根组织名称
    3: string thirdRootId;                  // 自定义第三方根组织的id
    4: i64 syncInterval;                    // 同步时间间隔
    5: i64 spaceSize;                       // 用户配额空间
    6: i32 userType;                        // 用户类型
}

// 审核员策略配置信息
struct ncTAuditStrategyInfo
{
    1: string                 auditorId;    // 审核员id
    2: string                 auditorName;  // 审核员名称
    3: bool                   checkCSFLevel;// 检查审核员密级
    4: list<ncTAuditObject>         obj;    // 审核对象
}

// 共享文档免审核的部门信息
struct ncTAuditWhiteListItem {
    1: string departmentId;                 // 部门ID
    2: string departName;                   // 部门名
    3: bool isEnable;                       // 是否启用
}

// 跨网络交换/文档库内外网同步共享范围限制类型
enum ncTDocExchangeLimitType {
    NCT_DOC_EXCHANGE = 1,                   // 限制跨网络交换文档范围
    NCT_LIB_SYNC = 2,                       // 限制文档库内外网同步文档范围
    NCT_DOC_EXCHANGE_AND_LIB_SYNC = 3       // 限制跨网络交换和文档库内外网同步文档范围
}

// 跨网络交换/文档库内外网同步信息
struct ncTDocExchangeInfo {
    1: string                   objId;      // 对象ID
    2: ncTAuditObjectType       objType;    // 类型
    3: string                   objName;    // 对象名称
    4: ncTDocExchangeLimitType  limitType;  // 限制类型
}

// 数据交换接收区
struct ncTDocExchangeRecvArea {
    1: optional string                   recvAreaId;         // 接收区Id、发送目录
    2: required string                   recvAreaName;       // 接收区名称
    3: required string                   recvAreaKey;        // 接收区密钥
    4: optional string                   docNameImportInfo;  // 接收区文档库名导入信息
    5: optional bool                     autoSend;           // 自动发送
}

// 设置了下载水印的文档库信息
struct ncTWatermarkDocInfo {
    1: string                 objId;          // 对象ID
    2: string                 objName;        // 对象名称
    3: i32                    objType;        // 对象类型 1：个人文档，3：自定义文档库, 5：归档库
    4: i32                    watermarkType;  // 水印类型，0为无水印(暂时不用，因为设置文档库为非水印文档库时会删除这条记录) ，1为预览，2为下载，3为预览与下载
}

// 定义设备类型，与shareserver服务ncIACSDeviceManager.idl文件中ncOSType保持一致
enum ncTDeviceOsType{
    NCT_UNKNOWN = 0,
    NCT_IOS = 1,
    NCT_ANDROID = 2,
    NCT_WINDOWSPHONE = 3,
    NCT_WINDOWS = 4,
    NCT_MACOSX = 5,
    NCT_WEB = 6,
    NCT_MOBILEWEB = 7,
}

// 设备类型禁止登录信息
struct ncTOSTypeForbidLoginInfo {
    1: ncTDeviceOsType        osType;       // 设备类型
    2: bool                   status;       // 类型
}

// 第三方认证配置
struct ncTThirdPartyAuthConf {
    1:string thirdPartyId;              // 唯一标识第三方认证系统
    2:string thirdPartyName;            // 第三方认证系统名称
    3:bool enabled;                     // 开启状态
    4:string config;                    // 需要单独配置的信息，采用json string来保存
}

// 插件类型
enum ncTPluginType {
    AUTHENTICATION = 0,                 // 认证插件
    MESSAGE = 1,                        // 消息推送插件
}

// 多因子认证类型
enum ncTMFAType {
    SMSAuth = 0,                       // 短信认证
    OTPAuth = 1,                       // 一次性密码认证
}

// 第三方插件信息，在磁盘路径如下
// /sysvol/plugin/auth-1/auth_module.py、ou_module.py
//               /msg-3/msg_module.py
//               /msg-5/msg_module.py
struct ncTThirdPartyPluginInfo {
    1: i64 indexId;                      // 索引Id，用于确定插件在磁盘的位置
    2: string thirdPartyId;              // 唯一标识第三方认证系统
    3: string filename;                  // 文件名
    4: string data;                      // 文件内容
    5: ncTPluginType type;               // 插件类型 0:认证 1:消息推送
    6: string objectId;                  // 对象存储ID，用于确定插件在存储的位置
}

// 第三方应用配置
struct ncTThirdPartyConfig {
    1: i64 indexId;                      // 唯一索引
    2: string thirdPartyId;              // 唯一标识第三方认证系统
    3: string thirdPartyName;            // 第三方认证系统名称
    4: bool enabled;                     // 开启状态
    5: string config;                    // 需要单独配置的信息，采用json string来保存
    6: string internalConfig;            // 内部配置，不开放
    7: ncTThirdPartyPluginInfo plugin;   // 插件信息
}

// 第三方鉴权信息
struct ncTThirdToolAuthInfo{
    1:string appid;          //唯一标识
    2:string appkey;         //密钥
}

// 第三方预览工具配置信息
struct ncTThirdPartyToolConfig {
    1:string thirdPartyToolId;          //第三方工具标识
    2:bool enabled;                     //开启状态
    3:string url;                       //url
    4:string thirdPartyToolName;        //第三方工具名称
    5:optional ncTThirdToolAuthInfo authInfo;    //鉴权信息

    /*
    第三方工具标识如下:
    "CAD"
    "OFFICE"
    "ANYROBOT"
    "WOPI"
    "ASPOSE"

    工具标识为"CAD"时，合法的第三方工具名称为 "hc" 或 "mx"
    */
}

// 访问者信息
struct ncTAccessorInfo
{
    1: string id;                       // 访问者id
    2: i32 type;                        // 访问者类型 1:用户, 2:部门
    3: string name;                     // 访问者名称
}

// 网段信息
struct ncTNetInfo
{
    1: string ip;                       // ip
    2: string subNetMask;               // 子网掩码
    3: string id;                       // 网段id
}

// 网段访问者信息
struct ncTNetAccessorsInfo
{
    1: string id;                       // 用户网段设置id
    2: ncTNetInfo net;                  // 网段设置
    3: list<ncTAccessorInfo> accessors; // 访问者设置
}

// 文档库信息
struct ncTDocInfo
{
    1: string id;                       // 文档库id
    2: string name;                      // 文档库名称
}

// 用户设备信息
struct ncTLoginAccessDeviceInfo {
    1: string       udid;             // 设备唯一标识号
    2: i32          osType;           // 设备类型
    3: i32          disableFlag;      // 禁用标识
    4: i32          bindFlag;         // 绑定标识
}

// 用户登录访问控制信息
struct ncTUserLoginAccessControl
{
    1:list<ncTNetInfo> net;         // 网络访问控制
    2:list<ncTLoginAccessDeviceInfo> device;  // 登录设备信息
}

// 验证码类型
enum ncTVcodeType {
    IMAGE_VCODE = 1,        // 图片验证码
    NUM_VCODE = 2,          // 数字验证码
    DAUL_AUTH_VCODE = 3,    // 双因子认证短信验证码
}

// 获取发送MFA短信验证码后的返回信息
struct ncTReturnInfo {
    1: required string       telNumber;      // 手机号
    2: required i32          sendInterval;   // 发送间隔
    3: required bool         isDuplicateSended;   // 是否重复发送验证码了
}

// 用户登录附带选项信息
struct ncTUserLoginOption
{
    1: optional string       loginIp;             // 用户登录ip
    2: optional string       uuid;                // 验证码唯一标识
    3: optional string       vcode;               // 验证码字符串
    4: optional bool         isModify;            // 是否为修改密码界面
    5: optional bool         isPlainPwd;          // 是否为明文密码
    6: optional ncTVcodeType vcodeType;           // 验证码类型
    7: optional string       OTP;                 // oneTimePassword
}

// 用户修改密码附带选项信息
struct ncTUserModifyPwdOption
{
    1: optional string       uuid;                // 验证码唯一标识
    2: optional string       vcode;               // 验证码字符串
    3: optional bool         isForgetPwd;         // 是否忘记密码
}

// 文档审核模式
enum ncTDocAuditType {
    NCT_DAT_ONE = 1,        // 同级审核，一个人审核通过即可
    NCT_DAT_ALL = 2,        // 汇签审核，全部通过才算通过
    NCT_DAT_LEVEL = 3,      // 逐级审核，一级一级通过
    NCT_DAT_FREE = 4,       // 免审核
}

// 创建流程参数
struct ncTDocAuditInfo {
    1: optional string processId;           // 流程id
    2: required string name;                // 流程名称
    3: required ncTDocAuditType auditType;  // 审核模式
    4: required list<string> auditorIds;    // 如果是同级/汇签审核，表示所有的审核员；如果是逐级审核，auditorIds[0]表示第一级审核，依次类推
    5: required string destDocId;           // 审核通过后，存放的gns路径
    6: optional string creatorId;           // 创建者id
    7: optional bool status;                // 有效状态
    8: optional list<string> auditorNames;  // 审核员名称
    9: optional string creatorName;         // 创建者名称
    10: optional string destDocName;        // 文档路径名称
    11: optional list<ncTAccessorInfo> accessorInfos;     // 流程适用的范围，限定哪些部门，哪些人可以看到该流程
}

// anyshare所支持的外部应用
enum ncTExtAppType {
    NCT_CHAOJIBIAOGE = 1,        // 超级表格
}

// 用户管控密码配置
struct ncTUsrmPwdControlConfig {
    1: required bool pwdControl;        // 密码管控
    2: required string password;        // 设置密码
    3: required bool lockStatus;        // 账号锁定状态
}

// ntlm返回结构
struct ncTNTLMResponse {
    1: required string userId;
    2: required string sessKey;
}

// NAS 挂载路径结构体
struct ncTNASMountInfo {
    1: string mountName;                // 挂载路径
    2: string gns;                      // 挂载gns
    3: string gnsName;                  // 挂载gns名称
}

// 限速配置管理对象
struct ncTLimitRateObject
{
    1: string objectId;                    // 限速对象id
    2: string objectName;                  // 限速对象名称
}

// 限速配置类型
enum ncTLimitRateType {
    LIMIT_USER = 0,                         // 用户级别限速
    LIMIT_USER_GROUP = 1,                   // 用户组总体限速
}

// 限速配置信息
struct ncTLimitRateConfig {
    1: bool isEnabled;                      // 是否开启限速配置
    2: ncTLimitRateType limitType;          // 限速配置类型
}

// 限速配置管理信息
struct ncTLimitRateInfo {
    1: string id;                           // 限速配置唯一标识
    2: i32  uploadRate;                     // 最大上传速度
    3: i32  downloadRate;                   // 最大下载速度
    4: list<ncTLimitRateObject> userInfos;  // 用户列表
    5: list<ncTLimitRateObject> depInfos;   // 部门列表
    6: ncTLimitRateType limitType;          // 限速配置类型
}

// 已存在限速规则的对象信息
struct ncTLimitRateObjInfo {
    1: list<ncTLimitRateObject> userInfos;  // 已有规则的用户列表
    2: list<ncTLimitRateObject> depInfos;   // 已有规则的部门列表
}

// 第三方标密系统配置
struct ncTThirdCSFSysConfig {
    1: bool isEnabled;                      // 是否使用第三方标密系统
    2: string id;                           // 第三方标密系统id
    3: bool only_upload_classified;         // 仅上传已标密文件（启用文件上传定密勾选项参数）
    4: bool only_share_classified;          // 仅共享已标密文件
    5: bool auto_match_doc_classfication;   // 上传自动识别密级（启用自动识别文件密级勾选项参数）
}

// 内外链共享模板类型
enum ncTTemplateType {
    INTERNAL_LINK = 0,                          // 内链
    EXTERNAL_LINK = 1                           // 外链
}

// 内外链共享模板信息
struct ncTLinkTemplateInfo {
    1: string templateId;                   // 模板策略ID（添加接口传空）
    2: ncTTemplateType templateType;        // 模板类型
    3: list<ncTLinkShareInfo> sharerInfos;  // 共享者信息
    4: string config;                       // 模板配置信息
    5: required i64 createTime;             // 创建时间
}

// 外链共享信息
struct ncTExternalLinkInfo {
    1: string userId;                        // 用户ID
    2: i32 permValue;                        // 权限值
    3: string password;                      // 密码
    4: i32 allowExpireDays;                  // 配置天数
    5: i32 accessLimit;                      // 外链访问次数上限
}

// 文档下载限制配置管理对象
struct ncTDocDownloadLimitObject
{
    1: string objectId;                    // 限速对象id
    2: string objectName;                  // 限速对象名称
}

// 文档下载限制配置管理信息
struct ncTDocDownloadLimitInfo {
    1: string id;                                   // 唯一标识
    2: i64 limitValue;                              // 最大允许的单日下载量
    4: list<ncTDocDownloadLimitObject> userInfos;   // 用户列表
    5: list<ncTDocDownloadLimitObject> depInfos;    // 部门列表
}

// 文档类型
enum ncTDocType {
    NCT_USER_DOC = 1,           // 个人文档
    NCT_CUSTOM_DOC = 3,         // 文档库
    NCT_SHARE_DOC  = 4,         // 共享文档
    NCT_ARCHIVE_DOC = 5,        // 归档库
}

// 自动禁用配置
struct ncTUserAutoDisableConfig {
    1: bool isEnabled;           // 是否开启
    2: i32 days;                // 设置多大时间未登陆自动禁用
}

struct ncTRetainOutLinkVCode {
    1: string vCode;            // 进行外链留底审计的管理员验证码，权责集中模式下为系统管理员；权责分离模式下为审计管理员
    2: string securitVCode;     // 安全管理员验证码，权责分离模式下需要填写该项
}

// 绑定状态搜索范围
enum ncTBindStatusSearchScope{
    NCT_ALL = 1,                                // 所有状态
    NCT_BIND = 2,                               // 绑定状态
    NCT_UNBIND = 3,                             // 未绑定状态
}

// 定义设备绑定的用户信息
struct ncTDeviceBindUserInfo {
    1: string id;
    2: string displayName;
    3: string loginName;
    4: bool bindStatus;
}

// 登录验证码配置参数
struct ncTVcodeConfig {
    1: required bool isEnable;        // 开启关闭登录验证码功能。 true - 开启，false - 关闭。
    2: required i32 passwdErrCnt;     // 达到开启登录验证码的用户密码出错次数
}

// 生成的验证码信息
struct ncTVcodeCreateInfo {
    1:required string vcode;      // 经过 base64 编码后的验证码图片字符串
    2:required string uuid;       // 验证码唯一标识
    3:optional bool isDuplicateSended;   // 是否重复发送验证码了
}

// 回收站配置
struct ncTRecycleInfo {
    1: required string gns;         // 回收站 gns
    2: required string setter;      // 配置者
    3: required i32 retentionDays;  // 保留天数
}

// 允许用户搜索范围, 和shareserver服务ncIACSShareMgnt.idl文件中ncACSSearchRange保持一致
enum ncTSearchRange {
    NCT_LOGIN_NAME = 1,             // 只允许搜索用户名
    NCT_DISPLAY_NAME = 2,           // 只允许搜索显示名
    NCT_LOGIN_AND_DISPLAY = 3,      // 允许搜索用户名或显示名
}

// 搜索结果显示方式
enum ncTSearchResults {
    NCT_DISPLAY_NAME = 1,           // 搜索结果只显示显示名
    NCT_LOGIN_AND_DISPLAY = 2,      // 搜索结果显示用户名和显示名
}

// 共享时搜索用户配置
struct ncTSearchUserConfig {
    1: required bool exactSearch;                       // 模糊/精确搜索
    2: required ncTSearchRange searchRange;             // 允许用户搜索范围
    3: required ncTSearchResults searchResults;         // 搜索结果显示方式
}

// 优先访问配置
struct ncTPriorityAccessConfig {
    1: required bool isEnable;          // 是否开启优先访问功能
    2: required i32 limitCPU;           // CPU使用率的阈值
    3: required i32 limitMemory;        // 内存使用率的阈值
    4: required i32 limitPriority;      // 用户权重的阈值
}

// 活跃用户数信息
struct ncTActiveUserInfo {
    1: required string time;                            // 时间
    2: required i64 activeCount;                        // 用户活跃数
    3: required double userActivity;                    // 用户活跃度
}

// 活跃报表信息
struct ncTActiveReportInfo {
    1: required i64 avgCount;                           // 平均活跃数
    2: required double avgActivity;                     // 平均活跃度
    3: required list<ncTActiveUserInfo> userInfos;      // 活跃用户数信息
}

// 第三方根节点信息
struct ncTThirdPartyRootNodeInfo {
    1: string name;                             // 根组织名称
    2: string thirdId;                          // 根组织第三方id
}

// 第三方用户信息
struct ncTUsrmThirdPartyUser {
    1: string loginName;                        // 登录名
    2: string displayName;                      // 显示名
    3: string thirdId;                          // 第三方用户id
    4: string deptThirdId;                      // 第三方父部门id
}

// 第三方组织单位信息
struct ncTUsrmThirdPartyOU {
    1: string name;                             // 组织名称
    2: string thirdId;                          // 第三方部门id
    3: string parentThirdId;                    // 第三方父部门id
    4: bool importAll;                          // 是否导入组织下的所有子组织及用户，True--导入，False--只导入此组织
}

// 第三方节点信息
struct ncTUsrmThirdPartyNode {
    1: list<ncTUsrmThirdPartyOU> ous;           // 组织
    2: list<ncTUsrmThirdPartyUser> users;       // 用户
}

// 文档抓取配置
struct ncTFileCrawlConfig {
    1: i32      strategyId;         // 策略Id
    2: string   userId;             // 用户Id
    3: string   loginName;          // 用户登录名
    4: string   displayName;        // 用户显示名
    5: string   docId;              // 目的文档库docId，为空表示文档库已失效
    6: string   docName;            // 文档库名称
    7: string   fileCrawlType;      // 抓取文档类型，形如：".doc .txt .ppt"
}

// 自动归档策略配置对象
struct ncTAutoArchiveObjInfo
{
    1: string id;                               // 对象id
    2: string name;                             // 对象名
}

// 自动归档策略配置
struct ncTAutoArchiveConfig
{
    1: string strategyId;                       // 策略ID
    2: list<ncTAutoArchiveObjInfo> users;       // 用户列表
    3: list<ncTAutoArchiveObjInfo> departs;     // 部门列表
    4: i64 archiveCycle;                        // 归档周期，天数
    5: i64 archiveCycleModifyTime;              // 归档周期的变更时间
    6: string archiveDestDocId;                 // 目的归档库gns，归档库不存在，返回为空
    7: i64 archiveNextTime;                     // 下次归档时间，微秒的时间戳，前端可以根据设计显示精度
}

// 管理员开启并设置数据在回收站中的时间配置
struct ncTGlobalRecycleRetentionConfig{
	1: bool isEnable;	// 是否开启回收站数据保留
	2: i32 days;		// 回收站中数据保留时间（天数）
}

// 自动清理策略配置对象
struct ncTAutoCleanObjInfo
{
    1: string id;   // 对应的是数据库里面的f_obj_id，普通情况下保存userid/departmentid
    2: string name;
}

// 自动清理策略配置
struct ncTAutoCleanConfig
{
    1:  string strategyId;                   // 策略id
    2:  list<ncTAutoCleanObjInfo> users;     // 用户列表
    3:  list<ncTAutoCleanObjInfo> departs;   // 部门列表
    4:  i64 cleanCycleDays;                  // 清理周期，天数
    5:  i64 cleanCycleModifyTime;            // 策略更新时间
    6:  i64 cleanNextTime;                   // 下次清理时间
    7:  bool enableRemainHours;              // 启用数据保留时间
    8:  i64 remainHours;                     // 数据保留时间，小时
    9:  i64 createTime;                      // 策略创建时间
    10: bool status;                         // 策略的启用/禁用标志位（仅用于默认策略生效）
}

// 病毒文件处理类型
enum ncTVirusProcessType {
    NCT_VIRUS_DELETE = 0,        // 删除
    NCT_VIRUS_FIX = 1,           // 修复
}

// 站点病毒库更新类型
enum ncTVirusUpdateMethodType{
    MULTISITE_UPDATE = 0,
    FTP_UPDATE = 1,
}

// 文件染毒信息
struct ncTVirusInfo {
    1: string                 fileName;         // 文件名
    2: string                 virusName;        // 病毒名称
    3: string                 riskType;         // 风险类型
    4: ncTVirusProcessType    processType;      // 病毒文件处理类型
    5: string                 parentPath;       // 文件原父路径
    6: i64                    startTime;        // 开始时间
    7: i64                    endTime;          // 结束时间
}

// 扫描任务状态
enum ncTScanTaskStatus {
    NCT_NOT_START = 0,           // 未开始
    NCT_INITING = 1,             // 初始化中
    NCT_RUNNING = 2,             // 扫描中
    NCT_STOP = 3,                // 暂停
    NCT_FINISH = 4,              // 已完成
}

// 扫描类型
enum ncTScanType {
    NCT_SCAN_TYPE_ALL = 0,       // 全盘扫描
    MCT_SCAN_TYPE_CUSTOM = 1,    // 自定义扫描
}

// 扫描范围
struct ncTScanScope {
    1: list<string> userIds;
    2: list<string> departIds;
    3: list<string> cids;
}

// 扫描结果
struct ncTScanTaskInfo {
    1: string                 scanFilePath;     // 正在扫描的文件路径
    2: i64                    scanFileCount;    // 已扫描文件数
    3: i64                    useTime;          // 已使用时间，单位：秒
    4: i64                    startTime;        // 开始时间
    5: i64                    endTime;          // 结束时间
    6: double                 progressRate;     // 扫描进度
    7: ncTScanTaskStatus      status;           // 扫描任务状态
    8: ncTScanType            scanType;         // 扫描类型
    9: ncTScanScope           scanScope;        // 初始扫描范围
    10: string                nodeIP;           // 扫描节点IP
    11: string                nodeId;           // 扫描节点Id
}

// 病毒库信息
struct ncTVirusDBInfo {
    1: string                 virusDBName;      // 病毒库名称
    2: string                 virusDBData;      // 病毒库数据
    3: i64                    updateTime;       // 更新时间
}

// 本地同步策略配置对象
struct ncTLocalSyncObjInfo
{
    1: string id;                            // 对象id
    2: string name;                          // 对象名
}

// 本地同步策略配置
struct ncTLocalSyncConfig
{
    1: string strategyId;                       // 权限共享范围策略信息ID
    2: bool openStatus;                         // 是否开启本地同步配置
    3: bool deleteStatus;                       // 是否允许删除配置的同步任务
    4: list<ncTLocalSyncObjInfo> users;         // 用户列表
    5: list<ncTLocalSyncObjInfo> departs;       // 部门列表
    6: i64 createTime;                          // 创建时间
}

// webhook 配置信息
struct ncTWebhookConfig {
    1: required bool            isEnabled;      // 是否使用 webhook 通知
    2: required string          endpointURL;    // 第三方接收通知的 URL
}

// 错误码
enum ncTShareMgntError {
    NCT_DB_OPERATE_FAILED = 10001,                               //数据库执行失败
    NCT_UNKNOWN_ERROR = 10002,                                   //未知错误

    NCT_INVALID_URL = 20001,                                     //Url参数错误
    NCT_START_LESS_THAN_ZERO = 20002,                            //起始位置小于0
    NCT_START_MORE_THAN_TOTAL = 20003,                           //起始位置超过总数
    NCT_LIMIT_LESS_THAN_MINUS_ONE = 20004,                       //限制数量小于-1
    NCT_INVALID_DATETIME = 20005,                                //日期时间不合法

    NCT_INVALID_LOGIN_NAME = 20101,                              //登录名参数错误
    NCT_INVALID_DISPLAY_NAME = 20102,                            //显示名参数错误
    NCT_INVALID_EMAIL = 20103,                                   //email参数错误
    NCT_INVALID_PHONE_NUM = 20104,                               //手机号码参数错误
    NCT_DUPLICATED_LOGIN_NAME = 20105,                           //登录名已存在
    NCT_DUPLICATED_EMALI = 20106,                                //email已存在
    NCT_USER_NOT_ADMIN = 20107,                                  //用户不是部门、组织管理员
    NCT_INVALID_ACCOUNT_OR_PASSWORD = 20108,                     //用户账号或密码不正确
    NCT_USER_DISABLED = 20109,                                   //用户被禁用
    NCT_USER_NOT_EXIST = 20110,                                  //用户不存在
    NCT_USER_HAS_EXIST = 20111,                                  //用户已存在
    NCT_CANNOT_MOVE_USER_TO_UNDISTRIBUTE_GROUP = 20112,          //不能移动用户到未分配组
    NCT_GROUP_NOT_EXIST = 20113,                                 //联系人组不存在
    NCT_GROUP_HAS_EXIST = 20114,                                 //联系人组已存在
    NCT_CANNOT_MODIFY_NONLOCAL_USER_PASSWORD = 20115,            //当前用户是外部用户,不支持修改密码
    NCT_CHECK_PASSWORD_FAILED = 20116,                           //检查用户密码失败
    NCT_INVALID_GROUP_NAME = 20117,                              //无效的组名
    NCT_CANNOT_OPERATE_TMP_GROUP = 20118,                       //不能操作临时组
    NCT_CANNOT_FIND_LOGINNAME_OR_EMAIL = 20119,                 //未发现登录名或邮箱
    NCT_CANNOT_ADD_SELF_TO_GROUP = 20120,                       //不能添加自己为联系人
    NCT_CONTACT_HASE_EXIST = 20121,                             //联系人已存在
    NCT_CONTACT_NOT_EXIST = 20122,                              //联系人不存在
    NCT_DUPLICATED_DISPLAY_NAME = 20123,                        //显示名已存在
    NCT_INVALID_USER_PRIORITY = 20124,                          //非法的用户排序权重值，必须在[1, 999]之间
    NCT_INVALID_PASSWORD = 20125,                               //非法的普通密码
    NCT_INVALID_STRONG_PASSWORD = 20126,                        //非法的强密码
    NCT_PASSWORD_EXPIRE = 20127,                                //密码已过期
    NCT_PASSWORD_NOT_SAFE = 20128,                              //密码不安全
    NCT_PASSWORD_IS_INITIAL = 20129,                            //密码是初始密码
    NCT_ACCOUNT_LOCKED = 20130,                                 // 账号已被锁定 (非涉密)
    NCT_PWD_FIRST_FAILED = 20131,                               // 第一次密码错误
    NCT_PWD_SECOND_FAILED = 20132,                              // 第二次密码错误
    NCT_INVALID_SAPCE_SIZE = 20133,                             // 无效的配额空间
    NCT_WRONG_PASSWORD = 20134,                                 // 用户密码错误
    NCT_PWD_THIRD_FAILED = 20135,                               // 到达密码错误最大次数，帐号将被锁定(非涉密模式)
    NCT_CANNOT_MODIFY_CONTROL_PASSWORD = 20136,                 // 开启密码管控的用户不能修改密码
    NCT_CONTROLED_PASSWORD_EXPIRE = 20137,                      // 开启密码管控的用户密码过期
    NCT_SPACE_ALLOCATED_FOR_USER_EXCEEDS_THE_MAX_LIMIT = 20138, // 当前用户管理可分配空间已超出限制
    NCT_CANNOT_LOGIN_SLAVE_SITE = 201239,                       // 不能登录分站点
    NCT_INVALID_USER_TYPE = 201240,                             // 用户类型非法
    NCT_USER_LOGIN_IP_RESTRICTED = 201241,                      // 用户登录ip被限制
    NCT_INVALID_PASSWORD_ERR_CNT = 201242,                      // 用户密码有效值为[1,99]
    NCT_ACCOUNT_CANNOT_LOGIN_IN_SECRET_NODE = 20145,            // 系统未初始化，管理员账号不能登录 (涉密模式)
    NCT_UNINSTALL_PWD_NOT_ENABLED = 20146,                      // 卸载口令功能未启用
    NCT_UNINSTALL_PWD_INCORRECT = 20147,                        // 卸载口令功能不正确
    NCT_CHECK_USER_TOKEN_FAILED = 20148,                        // 检查用户token认证失败
    NCT_CHECK_VCODE_IS_NULL = 20149,                            // 用户未输入验证码
    NCT_CHECK_VCODE_IS_TIMEOUT = 20150,                         // 验证码已失效
    NCT_CHECK_VCODE_IS_WRONG = 20151,                           // 验证码错误
    NCT_USER_NOT_SUPER_ADMIN = 20152,                           // 用户不是超级管理员
    NCT_REMAIN_ADMIN_ACCOUNT = 20153,                           // 保留管理员账号
    NCT_ACCOUNT_CONFICT_WITH_ADMIN = 20154,                     // 新建账号与管理员账号冲突
    NCT_RESPONSIBLE_PERSON_EXIST = 20155,                       // 部门负责人已存在
    NCT_INVALID_STRONG_PWD_LENGTH = 20156,                      // 强密码长度最小有效值为[8-99]
    NCT_USER_ACCOUNT_HAS_EXPIRED = 20157,                       // 用户账号已过期
    NCT_INVALID_REMARK = 20158,                                 // 备注不合法
    NCT_INVALID_IDCARDNUMBER = 20159,                           // 身份证号不合法
    NCT_DUPLICATED_IDCARDNUMBER = 20160,                        // 身份证号重复
    NCT_CHECK_VCODE_MORE_THAN_THE_LIMIT = 20161,                // 验证码输错超过3次失效
    NCT_OTP_WRONG = 20162,                                      // 动态密码错误
    NCT_MFA_OTP_SERVER_ERROR = 20163,                           // MFA动态密码服务器异常
    NCT_USER_HAS_NOT_BOUND_PHONE = 20164,                       // 用户未绑定手机
    NCT_PHONE_NUMBER_HAS_BEEN_CHANGED = 20165,                  // 用户绑定的手机号被更改
    NCT_OTP_TIMEOUT = 20166,                                    // 动态密码已过期
    NCT_OTP_TOO_MANY_WRONG_TIME = 20167,                        // 动态错误次数过多
    NCT_MFA_SMS_SERVER_ERROR = 20168,                           // MFA短信服务器异常
    NCT_INVALID_USER_SPACE = 20169,                             // 配额空间不合法
    NCT_INVALID_USER_STATUS = 20170,                            // 用户状态不合法

    NCT_DEPARTMENT_NOT_EXIST = 20201,                            // 部门不存在
    NCT_DEPARTMENT_HAS_EXIST = 20202,                            // 部门已存在
    NCT_INVALID_DEPART_NAME = 20203,                             // 无效的部门名
    NCT_ORGNIZATION_NOT_EXIST = 20204,                           // 组织不存在
    NCT_ORGNIZATION_HAS_EXIST = 20205,                           // 组织已存在
    NCT_INVALID_ORG_NAME = 20206,                                // 无效的组织名
    NCT_CANNOT_MOVE_DEPARTMENT_TO_UNDISTRIBUTE_GROUP = 20207,    // 不能移动部门到未分配用户组
    NCT_CANNOT_MOVE_DEPARTMENT_TO_ALL_GROUP = 20208,             // 不能移动部门到所有用户组
    NCT_CANNOT_MOVE_DEPARTMENT_TO_CHILDREN = 20209,              // 不能移动部门到它的子部门
    NCT_SRC_DEPARTMENT_NOT_EXIST = 20210,                        // 源部门不存在
    NCT_DEST_DEPARTMENT_NOT_EXIST = 20211,                       // 目的部门不存在
    NCT_DUPLICATED_SUBDEP_EXIST_IN_DEP = 20212,                  // 目的部门存在同名子部门
    NCT_USER_NOT_IN_DEPARTMENT = 20213,                          // 用户不在此部门
    NCT_CHECK_RESPONSE_ERROR = 20214,                            // 检查负责人失败
    NCT_ORG_OR_DEPART_NOT_EXIST = 20215,                         // 组织或部门不存在
    NCT_CANNOT_DELETE_DEPART = 20216,                            // 不能删除组织
    NCT_CANT_DEL_USER_CAUSE_USER_DOC_EXISTS = 20217,             // 无法删除用户 XXX，该账号仍有个人数据，请先关闭其个人文档，再执行此操作。
    NCT_INVALID_ORGAN_PRIORITY = 20218,                          // 非法的组织权重值，必须在[1, 999]之间
    NCT_INVALID_DEPART_PRIORITY = 20219,                         // 非法的部门权重值，必须在[1, 999]之间
    NCT_CANNOT_DELETE_DEPART_NO_PERM = 20220,                    // 当前账号没有权限执行此操作
    NCT_CANNOT_MANAGER_DEPARTMENT = 20221,                       // 组织或部门不在管辖范围内
    NCT_NOT_IN_ORIGINAL_DEPARTMENT = 20222,                      // 手动排序时必须在同一部门内
    NCT_DEST_POSTION_ILLEGAL = 20223,                            // 手动排序时传入的目标部门不存在

    NCT_BATCH_USERS_EXPORTING = 20301,                           // 正在导出用户
    NCT_BATCH_USERS_IMPORTING = 20302,                           // 正在导入用户
    NCT_CANNOT_SELECT_UNDISTRIBUTE_AND_ALL_GROUP = 20303,        // 不能选择未分配组和所有用户组
    NCT_WRONG_FILE_FORMAT = 20304,                               // 文件格式与给定的不符
    NCT_CANNOT_FILL_IN_DEFAUL_PASSWORD = 20305,                  // 非新增用户不能填写初始密码
    NCT_DOWNLOAD_BATCH_USERS_FAILED = 20306,                     // 下载批量用户失败
    NCT_DOWNLOAD_BATCH_USERS_TASK_NOT_EXIST = 20307,             // 批量用户任务不存在
    NCT_ORG_MANAGER_CANNOT_EDIT_OWN_AUTH_INFO = 20308,           // 组织管理员不能编辑自身的密级、配额

    NCT_INVALID_DOMAIN_PARAMETER = 20401,                        //域导入参数错误
    NCT_DOMAIN_NOT_EXIST = 20402,                                //域不存在
    NCT_DOMAIN_HAS_EXIST = 20403,                                //域已存在
    NCT_DOMAIN_USER_NOT_EXIST = 20404,                           //域用户不存在
    NCT_DOMAIN_USER_HAX_EXIST = 20405,                           //域用户已存在
    NCT_CANNOT_IMPORT_DOMAIN_USER_TO_UNDISTRIBUTE = 20406,      //不能导入域用户到未分配
    NCT_CANNOT_IMPORT_DOMAIN_USER_TO_ALL = 20407,               //不能导入域用户到所有用户组
    NCT_FAILED_CHECK_DOMAIN_USER = 24008,                       //域用户检查失败
    NCT_CANNOT_IMPORT_AGAIN = 20409,                            //不能重复导入
    NCT_DOMAIN_TYPE_NOT_MATCH = 20410,                          //域类型不匹配
    NCT_DOMAIN_SERVER_UNAVAILABLE = 20411,                      //连接域服务器失败
    NCT_DOMAIN_ERROR = 20412,                                   //域服务器错误
    NCT_DOMAIN_DISABLE = 20413,                                 //用户域被禁用
    NCT_FORBIDDEN_LOGIN = 20414,                                //禁止登录
    NCT_DOMAIN_CONFIF_PARAMETER = 20415,                        //域配置参数错误
    NCT_PARAMETER_IS_NULL = 20416,                              //参数为空
    NCT_DOMAIN_IMPORTING = 20417,                               //另一个域用户组织正在导入
    NCT_DOMAIN_NAME_CONFIF_ERROR = 20418,                       //域名配置错误
    NCT_THREAD_IMPORTING = 20419,                               //另一个第三方用户组织正在导入
    NCT_PARENT_DOMAIN_NOT_EXIST = 20420,                        //首选域不存在
    NCT_FAILOVER_NOT_MATCH_PARENT = 20421,                      //备用域与首选域不符
    NCT_DUPLICATED_FAILOVER_DOMAIN = 20422,                     //备用域地址不能相同
    NCT_FAILOVER_DOMAIN_ADDRESS_SAME_WITH_PARENT = 20423,       //备用域地址不能与主域相同

    NCT_USER_NUM_OVERFLOW = 20518,                              // 新建/导入的用户数超过授权数
    NCT_PRODUCT_NOT_AUTHORIZED = 20519,                         // 产品尚未授权
    NCT_PRODUCT_HAS_EXPIRED = 20524,                            // 产品授权已过期

    NCT_FAILED_THIRD_VERIFY = 20601,                             //第三方认证失败
    NCT_FAILED_THIRD_CONFIG = 20602,                             //第三方认证配置错误
    NCT_INVALID_APPID_OR_APPKEY = 20603,                         //无效的认证id或认证key
    NCT_THIRD_CONFIG_NOT_EXIST = 20604,                          //第三方配置不存在
    NCT_THIRD_CONFIG_HAS_EXIST = 20605,                          //第三方配置已存在
    NCT_THIRD_PARTY_AUTH_ERROR = 20606,                          //第三方认证系统错误
    NCT_THIRD_PARTY_AUTH_NOT_OPEN = 20607,                       //第三方验证没有开启
    NCT_CANNOT_CONNECT_THID_PARTY_SERVER = 20608                 //不能连接到第三方认证服务
    NCT_USER_NOT_EXIST_IN_LDAP = 20609,                          //LDAP服务器中不存在当前用户
    NCT_NEED_THIRD_OAUTH = 20610,                                //需要通过第三方认证网站进行登录
    NCT_USER_HAS_BEEN_DELETED = 20611,                           //用户已经被第三方认证系统删除
    NCT_THIRD_DB_NOT_EXISTS = 20612,                             //第三方数据库不存在
    NCT_THIRD_TABLE_NOT_EXISTS = 20613,                          //第三方表信息不存在
    NCT_TIMESTAMP_EXPIRED = 20614,                               //时间戳过期
    NCT_INVALID_THIRD_PARTY_PLUGIN = 20615,                      //非法的第三方插件
    NCT_INVALID_FILENAME = 20616,                                //非法的文件名
    NCT_THIRD_PLUGIN_INTER_ERROR = 20617,                        //第三方插件内部错误
    NCT_MFA_CONFIG_ERROR = 20618,                                //多因子认证配置错误

    NCT_INVALID_SECTION = 20701,                                // 非法的section
    NCT_INVALID_OPTION = 20702,                                 // 非法的option
    NCT_INVALID_VALUE = 20703,                                  // 非法的value
    NCT_OPTION_NOT_EXISTS = 20704,                              // option不存在
    NCT_SECTION_NOT_EXISTS = 20705,                             // section不存在

    NCT_SMTP_SEND_FAILED = 20801,                                // SMTP发送失败
    NCT_SHARER_IS_EMPTY = 20802,                                 // 共享者为空
    NCT_SHARE_SCOPE_IS_EMPTY = 20803,                            // 共享范围为空
    NCT_SHARE_STRATEGY_NOT_EXISTS = 20804,                       // 权限共享范围限制策略不存在
    NCT_USER_NOT_IN_PERM_SOCPE = 20805,                          // 用户不在权限共享范围内
    NCT_SMTP_PARAMETER_PARSE_FAILED = 20806,                     // 参数解析失败
    NCT_SMTP_SERVER_NOT_SET = 20807,                             // smtp服务器未设置
    NCT_SMTP_SERVER_NOT_AVAILABLE = 20808,                       // SMTP服务器不可用，请检查服务器地址、安全连接或端口是否正确
    NCT_SMTP_RECIPIENT_MAIL_ILLEGAL = 20809,                     // 收件人格式非法
    NCT_SMTP_LOGIN_FAILED = 20810,                               // 认证失败，登录名或密码错误
    NCT_SMTP_AUTHENTICATION_METHOD_NOT_FOUND = 20811,            // No suitable authentication method was found.
    NCT_INVALID_SERVER = 20812                                   // SMTP服务器名只能包含 英文、数字 及 @-_. 字符，长度范围 3~100 个字符，请重新输入
    NCT_INVALID_PORT = 20813                                     // 请输入1~65535范围内的整数
    NCT_INVALID_SAFEMODE = 20814                                 // safeMode只能输入0，1，2三个数字
    NCT_SMTP_PASSWORD_NOT_SET = 20815                            // 未输入邮箱密码


    NCT_INVALID_CSF_LEVEL = 20901,                              // 非法的密级等级
    NCT_SYS_CSF_LEVEL_CANT_DOWNGRADE = 20902,                   // 系统密级不能降低
    NCT_USER_CSF_LEVEL_CANT_BE_HIGHER_THAN_SYS = 20903,         // 用户密级不能高于系统密级
    NCT_DOC_CSF_LEVEL_CANT_BE_HIGHER_THAN_SYA = 20904,          // 文件密级不能高于系统密级
    NCT_CSF_LEVEL_ENUM_HAS_BEEN_INITIALIZED = 20905,            // 密级枚举已初始化
    NCT_CSF_LEVEL_ENUM_HAS_NOT_BEEN_INITIALIZED = 20906,        // 密级枚举尚未初始化

    NCT_INVALID_ACCESSOR_TYPE = 21001,                          // 非法的访问者类型，参见ncTAddLeakProofStrategyParam.accessorType
    NCT_ACCESSOR_ID_NOT_EXISTS = 21002,                         // 访问者不存在
    NCT_INVALID_PERM_VALUE = 21003,                             // 非法的权限值，参见ncTAddLeakProofStrategyParam.permValue
    NCT_STRATEGY_ID_NOT_EXISTS = 21004,                         // 策略id不存在
    NCT_ACCESSOR_ID_ALREADY_EXISTS = 21005,                     // 访问者已经已经存在

    NCT_PACKAGE_NAME_ERROR = 21100,                             // 包名长度不能大于150
    NCT_PACKAGE_NOT_EXIST = 21101,                              // 指定文件不存在
    NCT_PACKAGE_OS_ERROR = 21102,                               // 包OS类型验证失败
    NCT_PACKAGE_MODE_ERROR = 21103,                             // 包升级模式验证失败
    NCT_UPLOAD_EOSS_FAILED = 21104,                             // 上传EOSS失败
    NCT_INVALID_OS_PARAMETER = 21105,                           // 未识别的os适配系统参数,参数错误
    NCT_DEL_PKG_INFO_FAILED = 21106,                            // 删除升级包信息失败
    NCT_GET_URL_FAILED = 21107,                                 // 读取升级包URL失败

    APPID_NOT_EXIST = 21108,                                    // 第三方用户appid不存在
    APPID_DISABLED = 21109,                                     // 第三方用户appid未开启
    SIGN_AUTH_FAILED = 21110,                                   // 第三方用户签名认证失败
    APPID_HAS_EXIST = 21111,                                    // 第三方用户的appid已存在
    APPID_LENGTH_MORE_THAN_50 = 21112,                          // 第三方用户的appid长度不能超过50
    APPKEY_LENGTH_MORE_THAN_50_OR_EMPTY = 21113,                // 第三方appkey不能为空或长度不超过50

    NCT_AUDITOR_ALREADY_SET = 21201,                            // 审核员已经设置过
    NCT_INVALID_AUDIT_OBJECT = 21202,                           // 非法的审核对象
    NCT_AUDITOR_NOT_EXIST = 21203,                              // 审核员不存在
    NCT_AUDITOR_CSF_LEVEL_CHECK_FAILED = 21204,                 // 审核员密级不能低于系统密级
    NCT_AUDIT_OBJECT_TYPE_NOT_SUPPORT = 21205,                  // 审核对象类型不支持
    NCT_INVALID_DEPARTMENT_LIST = 21206,                        // 非法的部门列表
    NCT_CANT_SET_NONE_DIRECT_DEPART_STATUS = 21207,             // 不能设置非直属部门的状态
    NCT_CANT_OPERATE_AUDITOR_BECAUSEOF_SCOPE = 21208,           // 不能删除或设置不在自己范围内的审核员

    NCT_TOOL_ID_NOT_SUPPORT = 21301,                            // 第三方工具id不支持
    NCT_TOOL_ID_IS_EMPTY = 21302,                               // 第三方工具id不能为空
    NCT_URL_EMPTY = 21303,                                      // URL不能为空
    NCT_TOOL_NAME_NOT_SUPPORT = 21304,                          // 第三方工具name不支持

    NCT_INVALID_NET_ACCESSORS_PARAM = 21401,                    // 非法的用户网段访问设置参数
    NCT_INVALID_NET_IP_PARAM = 21402,                           // 网段ip非法
    NCT_INVALID_NET_MASK_PARAM = 21403,                         // 网段掩码非法
    NCT_INVALID_ACCESSOR_TYPE_PARAM = 21404,                    // 非法的访问者类型参数
    NCT_NET_ACCESSOR_ID_NOT_EXIST = 21405,                      // 网段访问者id不存在
    NCT_NET_ACCESSOR_EXIST = 21406,                             // 该网段设置已添加
    NCT_NET_ACCESSOR_DATA_ERROR = 21407,                        // 数据错误,id与ip存在不一致

    NCT_INVALID_CREATORID = 21501,                              // 非管理员无法创建审核流程
    NCT_INVALID_DOC_AUDIT_INFO_PARAM = 21502,                   // 非法的文档审核信息参数
    NCT_INVALID_DOC_AUDIT_TYPE = 21503,                         // 非法的文档审核模式
    NCT_INVALID_AUDITORS = 21504,                               // 非法的文档审核员
    NCT_INVALID_AUDITORS_OR_TYPE = 21505,                       // 审核模式与已设定审核员数量不匹配
    NCT_DOC_AUDIT_NAME_EXIST = 21506,                           // 文档审核流程已存在，不能重复添加
    NCT_DOC_AUDIT_PROCESS_ID_NOT_EXIST = 21507,                 // 文档审核流程id不存在
    NCT_INVALID_EDITORID = 21508,                               // 非创建者或admin没有权限修改
    NCT_INVALID_SEARCH_DOC_AUDIT_TYPE = 21509,                  // 非法的搜索文档审核流程关键字类型
    NCT_INVALID_AUDIT_PROCESS_NAME = 21510,                     // 非法的审核流程名
    NCT_INVALID_DEST_DOC_ID = 21511,                            // 非法的目的文档路径
    NCT_EDITORID_NOT_EXIST = 21512,                             // 编辑者已被删除
    NCT_EDITORID_DISABLED = 21513,                              // 编辑者已被禁用
    NCT_INVALID_MANAGER_ID = 21514,                             // 非法的管理员id
    NCT_DOC_AUDIT_PROCESS_IS_EMPTY = 21515,                     // 文档审核流程为空,未配置
    NCT_INVALID_ACCESSOR_INFOS = 21516,                         // 文档流程可见性配置错误，请检测用户或者部门id是否存在
    NCT_DEST_DOC_ID_TOO_DEEP = 21517,                           // 目的文档路径过深

    NCT_INVALID_EXT_APP_PARAMS = 21601,                         // 非法的外部应用调用参数
    NCT_INVALID_EXT_APP_TYPE = 21602,                           // 尚不支持外部应用
    NCT_INVALID_EXT_APP_CONFIG = 21603,                         // 获取外部应用配置失败
    NCT_EXT_APP_DISABLED = 21604,                               // 外部应用被禁用
    NCT_ENTER_EXT_APP_FAILED = 21605,                           // 跳转外部应用失败
    NCT_CONNECT_EXT_APP_FAILED = 21606,                         // 连接外部应用失败

    NCT_INVALID_RECEIVE_KEY = 21701,                            // 非法的数据接收密钥
    NCT_OBJ_NOT_EXIST = 21702,                                  // 对象不存在
    NCT_PARAMTER_IS_EMPTY = 21703,                              // 参数为空
    NCT_OBJ_EXIST = 21704,                                      // 对象已存在

    NCT_INVALID_GNS_PATH = 21801,                               // 挂载点gns路径不正确 （文档库不存在）
    NCT_DUPLICATE_MOUNT_POINT = 21802,                          // 重复的挂载点
    NCT_NOT_INACTIVATED = 21803,                                // 没有已激活的节点
    NCT_INVALID_PARAMTER = 21804,                               // 非法参数
    NCT_GET_NODE_LIST_FAILED = 21805,                           // 获取节点列表失败
    NCT_NODE_NOT_ONLINE = 21806,                                // 节点离线

    NCT_LIMIT_RATE_OBJECT_NOT_SET = 21901,                      // 限速对象未设置
    NCT_LIMIT_RATE_NOT_EXIST = 21902,                           // 该条限速配置不存在
    NCT_INVALID_LIMIT_RATE_VALUES = 21903,                      // 限速值不合法
    NCT_INVALID_LIMIT_RATE_TYPE = 21904,                        // 限速类型不合法
    NCT_ONLY_ONE_LIMIT_RATE_OBJECT = 21905,                     // 只允许设置一个限速对象
    NCT_LIMIT_USER_EXIST = 21906,                               // 用户已存在于列表中
    NCT_LIMIT_DEPART_EXIST = 21907,                             // 部门已存在于列表中
    NCT_AT_LEAST_SET_ONE_SPEED = 21908,                         // 至少设置一种最大传输速度

    NCT_INVALID_DOC_WATERMARK_CONFIG = 22001,                   // 文件水印配置不合法
    NCT_DOC_WATERMARK_DISABLED = 22002,                         // 文件水印未开启
    NCT_INVALID_WATERMARK_TYPE = 22003,                         // 水印类型错误

    NCT_INVALID_LINK_TEMPLATE_TYPE = 22101,                     // 模板类型错误
    NCT_INVALID_SHAERER_TYPE = 22102,                           // 共享者类型错误
    NCT_TEMPLATE_NOT_EXIST = 22103,                             // 模板不存在
    NCT_CANNOT_DELETE_DEFAULT_LINK_TEMPLATE = 22104,            // 禁止删除默认模板
    NCT_CANNOT_EDIT_DEFAULT_LINK_TEMPLATE_SHARER = 22105,       // 禁止编辑默认模板的共享者
    NCT_CANNOT_SET_OWNER = 22106,                               // 禁止设置为所有者
    NCT_EXCEED_MAX_INTERNAL_LINK_EXPIRE_DAY = 22107,            // 超过内链模板最大天数限制
    NCT_EXCEED_MAX_LINK_PERM = 22108,                           // 超出最大权限
    NCT_EXCEED_MAX_EXTERNAL_LINK_EXPIRE_DAY = 22109,            // 超出最大外链设置天数
    NCT_NEED_SET_ACCESS_PASSWORD = 22110,                       // 未设置访问密码
    NCT_EXCEED_MAX_EXTERNAL_LINK_EXPIRE_TIME = 22111,           // 超出最大访问次数

    NCT_NET_DOCS_LIMIT_ID_NOT_EXIST = 22201,                    // 网段文档库限制id不存在
    NCT_NET_DOCS_LIMIT_EXIST = 22202,                           // 网段文档库限制记录已存在
    NCT_DOC_ID_NOT_SET = 22203,                                 // 文档库id未设置

    NCT_DOC_DOWNLOAD_LIMIT_OBJECT_NOT_SET = 22204,              // 限速对象未设置
    NCT_DOC_DOWNLOAD_LIMIT_NOT_EXIST = 22205,                   // 该条限速配置不存在
    NCT_INVALID_DOC_DOWNLOAD_LIMIT_VALUE = 22206,               // 限速值不合法

    NCT_INVALID_DOC_TYPE = 22207,                               // 文档类型非法

    NCT_INVALID_CPU_USAGE_THRESHOLD = 22208,                    // 非法cpu使用率阈值
    NCT_INVALID_MEMORY_USAGE_THRESHOLD = 22209,                 // 非法内存使用率阈值
    NCT_INVALID_PRIORITY = 22210,                               // 非法权重值
    NCT_INSUFFICIENT_SYSTEM_RESOURCES = 22211,                  // 系统资源不足

    NCT_SITE_NOT_EXIST = 22305,                                 // 站点不存在

    NCT_EMAILADDR_NOT_SET = 22306,                              // 邮箱地址未设置
    NCT_SECURIT_EMAILADDR_NOT_SET = 22307,                      // 安全管理员邮箱地址未设置
    NCT_SITE_HAS_BEEN_MOVED = 22308,                            // 站点被移除

    NCT_INVALID_SEARCH_SCOPE = 22401,                           // 设备绑定管理搜索范围非法
    NCT_INVALID_SEARCH_CONFIG_PARAM = 22402,                    // 非法搜索配置

    NCT_INVALID_FILE_NAME = 22501,                              // 非法文件名
    NCT_INVALID_COMPRESS_PASSWORD = 22502,                      // 非强密码
    NCT_INVALID_ACTIVE_PARAM = 22503,                           // 导出活跃日志参数不合法
    NCT_INVALID_HISTORY_PARAM = 22504,                          // 导出历史日志参数不合法
    NCT_COMPRESS_TASK_FAILED = 22505,                           // 导出日志失败
    NCT_COMPRESS_TASK_IN_PROGRESS = 22506,                      // 导出任务进行中
    NCT_COMPRESS_TASK_NOT_EXIST = 22507,                        // 导出任务不存在
    NCT_DOWNLOAD_HISTORY_LOG_FAILED = 22508,                    // 下载历史日志出错

    NCT_INVALID_SMS_CONFIG = 22601,                             // 短信服务器配置不合法
    NCT_USER_NOT_ACTIVATE = 22602,                              // 账号已被禁用，是否立即激活
    NCT_INVALID_TEL_NUMBER = 22603,                             // 手机号不合法
    NCT_TEL_NUMBER_EXISTS = 22604,                              // 手机号已存在
    NCT_NOT_SUPPORT_SMS_SERVER = 22605,                         // 不支持的短信服务器类型
    NCT_USER_IS_ACTIVATE = 22606,                               // 账号已激活
    NCT_SMS_VERIFY_CODE_ERROR = 22607,                          // 验证码错误
    NCT_SMS_VERIFY_CODE_TIMEOUT = 22608,                        // 验证码过期
    NCT_SMS_ACTIVATE_DISABLED = 22609,                          // 短信激活未开启
    NCT_CONNECT_SMS_SERVER_ERROR = 22610,                       // 连接短信服务器失败
    NCT_SEND_VERIFY_CODE_FAIL = 22611,                          // 发送短信验证码失败

    NCT_DOWNLOAD_ACTIVE_REPORT_FAILED = 22701,                  // 下载活跃报表失败
    NCT_DOWNLOAD_ACTIVE_REPORT_IN_PROGRESS = 22702,             // 下载活跃报表进行中
    NCT_DOWNLOAD_ACTIVE_REPORT_NOT_EXIST = 22703,               // 下载活跃报表任务不存在

    NCT_INVALID_RECV_AREA_NAME = 22801,                         // 接收区名称不合法
    NCT_RECV_AREA_EXIST = 22802,                                // 接收区已存在
    NCT_RECV_AREA_NOT_EXIST = 22803,                            // 接收区不存在
    NCT_CREATE_SEND_DIR_ERROR = 22804,                          // 创建发送目录失败
    NCT_RECV_AREA_NAME_IS_EMPTY = 22805,                        // 接收区名称为空

    NCT_ROLE_NAME_EXIST = 22901,                                // 角色名已存在
    NCT_INVALID_ROLE_NAME = 22902,                              // 角色名非法
    NCT_INVALID_CREATOR = 22903,                                // 创建者非法
    NCT_ROLE_NOT_EXIST = 22904,                                 // 角色不存在
    NCT_INVALID_OPERATOR = 22905,                               // 操作者非法
    NCT_INVALID_MEMBER = 22906,                                 // 角色成员非法
    NCT_SYS_ROLE_CANNOT_SET_OR_DELETE = 22908,                  // 系统角色不允许设置或删除
    NCT_ROLE_MEMBER_NOT_EXIST = 22909,                          // 角色成员不存在

    NCT_FILE_CRAWL_STRATEGY_EXIST = 23001,                      // 文件抓取策略已存在
    NCT_CUSTOM_DOC_NOT_EXIST = 23002,                           // 文档库不存在

    NCT_AUTO_ARCHIVE_CONFIG_EXIST = 23101,                      // 对象已存在于另一条自动归档策略
    NCT_AUTO_ARCHIVE_CONFIG_NOT_EXIST = 23102,                  // 自动归档策略不存在
    NCT_AUTO_ARCHIVE_DEST_NOT_ARCHIVE_DOC = 23103,              // 自动归档目的位置不是归档库
    NCT_INVALID_AUTO_ARCHIVE_CONFIG = 23104,                    // 非法的自动归档策略参数

    NCT_CAN_NOT_DELETE_DEFAULT_AUTO_CLEAN_CONFIG = 23105,       // 禁止删除默认清理策略
    NCT_AUTO_CLEAN_CONFIG_NOT_EXIST = 23106,                    // 自动清理策略不存在
    NCT_AUTO_CLEAN_CONFIG_EXIST = 23107,                        // 对象已存在另一条自动清理策略

    NCT_UPDATE_ANTIVIRUS_TASK_STATUS_ERROR = 23201,             // 更新杀毒任务状态失败
    NCT_INVALID_TASK = 23202,                                   // 无效任务
    NCT_ANTIVIRUS_SERVER_DISABLED = 23203,                      // 杀毒服务未开启
    NCT_ANTIVIRUS_OPTION_LICENSE_EXPIRE = 23204,                // 杀毒选件已过期
    NCT_CANT_DELETE_ACTIVATED_ANTIVIRUS_LICENSE = 23205,        // 杀毒选件激活后禁止删除
    NCT_ANTIVIRUS_FTP_NOT_AVAILABLE = 23206,                    // 病毒库FTP服务器不可用
    NCT_ANTIVIRUS_FTP_LOGIN_FAILED = 23207,                     // 病毒库FTP认证失败
    NCT_ANTIVIRUS_FTP_NETWORK_ERROR = 23208,                    // 连接病毒库FTP服务器网络异常

    NCT_LOCAL_SYNC_CONFIG_EXIST = 23301,                        // 对象已存在于另一条本地同步策略
    NCT_LOCAL_SYNC_CONFIG_NOT_EXIST = 23302,                    // 本地同步策略不存在
    NCT_CAN_NOT_DELETE_DEFAULT_LOCAL_SYNC_CONFIG = 23303,       // 禁止删除默认本地同步策略
    NCT_INVALID_LOCAL_SYNC_CONFIG = 23304,                      // 非法的本地同步策略参数

    NCT_EXPORT_SPACE_REPORT_FAILED = 23401,                     // 导出用户空间使用情况报表失败
    NCT_EXPORT_SPACE_REPORT_IN_PROGRESS = 23402,                // 导出用户空间使用情况报表进行中
    NCT_EXPORT_SPACE_REPORT_NOT_EXIST = 23403,                  // 导出用户空间使用情况报表任务不存在
    NCT_HAVE_OTHER_SAME_TYPE_SPACE_REPORT_TASK_IN_PROGRESS = 23404,    // 存在其他相同类型的报表导出任务
    NCT_DOC_TYPE_NOT_SUPPORT_EXPORT = 23405,                    // 该文档库类型不支持导出功能

    NCT_OSS_NOT_EXIST = 24404,                                  // 对象存储不存在
    NCT_OSS_HAS_BEEN_DISABLED = 24405,                          // 对象存储已禁用
    NCT_NO_AVAILABLE_OSS = 24406,                               // 没有可用的对象存储
}

service ncTShareMgnt {
    // ----------------------------------------------------------------------------
    // 一、 组织管理
    // ----------------------------------------------------------------------------
    // 1.1 新建组织
    string Usrm_CreateOrganization(1: ncTAddOrgParam addParam) throws (1: EThriftException.ncTException exp)

    // 1.2 编辑组织
    void Usrm_EditOrganization(1: ncTEditDepartParam editParam) throws (1: EThriftException.ncTException exp)

    // 1.3 删除组织
    void Usrm_DeleteOrganization(1: string organId) throws (1: EThriftException.ncTException exp)

    // 1.4 根据组织id获取组织信息
    ncTUsrmOrganizationInfo Usrm_GetOrganizationById(1: string organId) throws (1: EThriftException.ncTException exp)

    // 1.5 根据组织名获取组织信息
    ncTUsrmOrganizationInfo Usrm_GetOrganizationByName(1: string organName) throws (1: EThriftException.ncTException exp)

    // 1.6 获取所管理的根组织获取根部门信息
    list<ncTRootOrgInfo> Usrm_GetSupervisoryRootOrg(1: string userId) throws(1: EThriftException.ncTException exp)

    // 1.7 根据用户ID获取所属的组织信息
    list<ncTRootOrgInfo> Usrm_GetRootOrgInfosByUserId(1: string userId) throws(1: EThriftException.ncTException exp)

    // ----------------------------------------------------------------------------
    // 二、 部门管理
    // ----------------------------------------------------------------------------
    // 2.1 新建部门
    string Usrm_AddDepartment(1: ncTAddDepartParam addParam) throws (1: EThriftException.ncTException exp)

    // 2.2 编辑部门
    void Usrm_EditDepartment(1: ncTEditDepartParam eidtParam) throws (1: EThriftException.ncTException exp)

    // 2.3 删除部门
    void Usrm_DeleteDepartment(1: string depart_id, 2:string manager_id) throws (1: EThriftException.ncTException exp)

    // 2.4 通过部门id获取部门信息
    ncTUsrmDepartmentInfo Usrm_GetDepartmentById(1: string depart_id) throws (1: EThriftException.ncTException exp)

    // 2.5 通过部门层级名获取部门信息
    ncTUsrmDepartmentInfo Usrm_GetDepartmentByName(1: string name) throws (1: EThriftException.ncTException exp)

    // 2.6 移动部门（例如：将部门depart01从父部门A移动到父部门B）
    void Usrm_MoveDepartment(1: string srcDepartId, 2: string destDepartId) throws (1: EThriftException.ncTException exp)

    // 2.7 获取子部门信息
    list<ncTDepartmentInfo> Usrm_GetSubDepartments(1: string departmentId) throws(1: EThriftException.ncTException exp)

    // 2.8 获取部门下的用户数
    i64 Usrm_GetDepartmentOfUsersCount(1: string departmentId) throws(1: EThriftException.ncTException exp)

    // 2.9 分页获取用户信息
    list<ncTUsrmGetUserInfo> Usrm_GetDepartmentOfUsers(1: string departmentId, 2: i32 start, 3: i32 limit)
                                                        throws(1: EThriftException.ncTException exp)

    // 2.10 批量添加用户到部门
    void Usrm_AddUserToDepartment(1: list <string> userIds, 2: string departmentId)
                                  throws(1: EThriftException.ncTException exp)

    // 2.11 移动用户（例如：将用户user01从父部门A移动到父部门B）
    list<string> Usrm_MoveUserToDepartment(1: list<string> userIds,
                                           2: string srcDepartId,
                                           3: string destDepartId)
                                           throws(1: EThriftException.ncTException exp)

    // 2.12 从部门中批量删除用户
    list<string> Usrm_RomoveUserFromDepartment(1: list <string> userIds, 2: string departmentId)
                                       throws(1: EThriftException.ncTException exp)

    // 2.13 在部门中根据key搜索用户，并返回分页数据
    list<ncTUsrmGetUserInfo> Usrm_SearchDepartmentOfUsers(1: string departmentId,
                                                          2: string searchKey,
                                                          3: i32 start,
                                                          4: i32 limit)
                                                          throws(1: EThriftException.ncTException exp)

    // 2.14 在部门中根据key搜索用户，并返回搜索的用户总数
    i64 Usrm_CountSearchDepartmentOfUsers(1: string departmentId,
                                          2: string searchKey)
                                          throws(1: EThriftException.ncTException exp)

    // 2.15 搜索我所管理的用户
    list<ncTSearchUserInfo> Usrm_SearchSupervisoryUsers(1: string managerid,
                                                        2: string key,
                                                        3: i32 start,
                                                        4: i32 limit)
                                                            throws(1: EThriftException.ncTException exp)

    // 2.16 获取我所管理的所有用户已使用的配额空间
    i64 Usrm_GetSupervisoryUsersUsedSpace(1: string managerid) throws(1: EThriftException.ncTException exp)

    // 2.17 定位用户
    list<ncTLocateInfo> Usrm_LocateUser(1: string managerid, 2: string userid)

    // 2.18 检查用户是否属于某个部门及其子部门
    bool Usrm_CheckUserInDepart(1: string userId, 2: string departId)
                                throws(1: EThriftException.ncTException exp)

    // 2.19 修改组织或部门对象存储
    void Usrm_EditDepartOSS(1: string departmentId, 2: string ossId) throws (1: EThriftException.ncTException exp)

    // 2.20 搜索所有部门
    list<ncTUsrmDepartmentInfo> Usrm_SearchDepartments(1: string userId, 2: string searchKey, 3: i32 start, 4: i32 limit) throws (1: EThriftException.ncTException exp)

    // 2.21 获取指定部门下最深层部门信息
    list<ncTUsrmDepartmentInfo> Usrm_GetDeepestDeparts(1: string departId) throws (1: EThriftException.ncTException exp)

    // 2.22 获取用户所管辖的部门
    list<ncTUsrmDepartmentInfo> Usrm_GetSupervisoryDeparts(1: string userId) throws (1: EThriftException.ncTException exp)

    // 2.23 根据部门ID(组织ID)获取部门信息（包含组织）
    ncTUsrmDepartmentInfo Usrm_GetOrgDepartmentById(1: string depart_id) throws (1: EThriftException.ncTException exp)

    // 2.24 通过部门第三方id获取部门信息
    ncTUsrmDepartmentInfo Usrm_GetDepartmentByThirdId(1: string third_id) throws (1: EThriftException.ncTException exp)

    // 2.25 获取指定部门下所有部门负责人信息
    list<ncTUsrmGetUserInfo> Usrm_GetDepartResponsiblePerson(1: string departId) throws (1: EThriftException.ncTException exp)

    // 2.37 批量根据部门ID(组织ID)获取部门（组织）父路经
    list<ncTUsrmDepartmentInfo> Usrm_GetDepartmentParentPath(1:list<string> departIds) throws (1: EThriftException.ncTException exp)

    // 2.38 对同级部门进行排序
    void Usrm_SortDepartment(1: string userId, 2: string srcDepartId, 3: string destUpDepartId) throws (1: EThriftException.ncTException exp)

    // ----------------------------------------------------------------------------
    // 三、 用户管理
    // ----------------------------------------------------------------------------
    // 3.1、新建用户
    string Usrm_AddUser(1:ncTUsrmAddUserInfo user, 2: string responsiblePersonId) throws (1: EThriftException.ncTException exp)

    // 3.2、编辑用户信息
    void Usrm_EditUser(1: ncTEditUserParam param, 2: string responsiblePersonId) throws (1: EThriftException.ncTException exp)

    // 3.3、编辑用户的权重排序
    void Usrm_EditUserPriority(1: string userId, 2: i32 priority) throws (1: EThriftException.ncTException exp)

    // 3.4、删除用户
    void Usrm_DelUser(1:string userId) throws (1: EThriftException.ncTException exp)

    // 3.5、根据用户id获取详细信息
    ncTUsrmGetUserInfo Usrm_GetUserInfo(1: string userId) throws(1: EThriftException.ncTException exp)

    // 3.6、根据用户登录名获取详细信息
    ncTUsrmGetUserInfo Usrm_GetUserInfoByAccount(1: string account) throws(1: EThriftException.ncTException exp)

    // 3.7、根据用户登录名获取用户id
    string Usrm_GetUserIdByAccount(1: string account) throws(1: EThriftException.ncTException exp)

    // 3.8、获取所有的用户总数
    i64 Usrm_GetAllUserCount () throws (1: EThriftException.ncTException exp)

    // 3.9、分页获取所有用户信息
    list<ncTUsrmGetUserInfo> Usrm_GetAllUsers(1: i32 start, 2: i32 limit) throws (1: EThriftException.ncTException exp)

    // 3.10、根据用户登录名修改用户密码
    void Usrm_ModifyPassword(1: string account,
                             2: string oldPassword,
                             3: string newPassword,
                             4: ncTUserModifyPwdOption option)
                             throws(1: EThriftException.ncTException exp)

    // 3.11、重置用户的密码
    void Usrm_ResetPassword(1:string userId) throws(1: EThriftException.ncTException exp)

    // 3.12、重置所有用户的密码
    void Usrm_ResetAllPassword(1: string password) throws(1: EThriftException.ncTException exp)

    // 3.13、设置用户密码配置信息
    void Usrm_SetPasswordConfig(1: ncTUsrmPasswordConfig pwdConfig) throws(1: EThriftException.ncTException exp)

    // 3.14、获取用户密码配置信息
    ncTUsrmPasswordConfig Usrm_GetPasswordConfig( ) throws(1: EThriftException.ncTException exp)

    // 3.15、启用|禁用用户
    void Usrm_SetUserStatus(1:string userId, 2:bool status) throws(1: EThriftException.ncTException exp)

    // 3.16、用户自注册
    string Usrm_SelfRegistration(1: string registerId,
                                 2: string certID,
                                 3: string realName,
                                 4: string pwd)
                                 throws(1: EThriftException.ncTException exp)

    // 3.17、编辑用户配额空间
    void Usrm_EditUserSpace(1: string userId,
                            2: i64 spaceSize,
                            3: string responsiblePersonId)
                            throws (1: EThriftException.ncTException exp)

    // 3.18、设置个人文档开启状态
    void Usrm_SetUserDocStatus(1: bool status) throws (1: EThriftException.ncTException exp)

    // 3.19、获取个人文档开启状态
    bool Usrm_GetUserDocStatus( ) throws (1: EThriftException.ncTException exp)

    // 3.20、设置默认配置空间大小
    void Usrm_SetDefaulSpaceSize(1: i64 spaceSize) throws (1: EThriftException.ncTException exp)

    // 3.21、获取默认配置空间大小
    i64 Usrm_GetDefaulSpaceSize() throws (1: EThriftException.ncTException exp)

    // 3.22 修改用户对象存储
    void Usrm_EditUserOSS(1: string userId, 2: string ossId) throws (1: EThriftException.ncTException exp)

    // 3.23 配置组织管理员的限额
    void Usrm_EditLimitSpace(1: string userId, 2: i64 limitUserSpaceSize, 3: i64 limitDocSpaceSize) throws (1: EThriftException.ncTException exp)

    // 3.24 更新组织管理员的已分配用户空间
    void Usrm_UpdateManagerDocSpace(1: string userId, 2: i64 spaceSize) throws (1: EThriftException.ncTException exp)

    // 3.25 更新组织管理员的已分配文档空间
    void Usrm_UpdateManagerUserSpace(1: string userId, 2: i64 spaceSize) throws (1: EThriftException.ncTException exp)

    // 3.26 批量修改配额前, 检查空间是否足够
    void Usrm_CheckHasEnoughSpace(1: list<string> userIds, 2: i64 spaceSize, 3: string responsiblePersonId) throws (1: EThriftException.ncTException exp)

    // 3.27 批量修改配额前, 通过部门id检查空间是否足够
    void Usrm_CheckSpaceByDeptId(1: string deptId, 2: bool enableSub, 3: i64 spaceSize, 4: string responsiblePersonId) throws (1: EThriftException.ncTException exp)

    // 3.28 检查文档空间是否足够
    void Usrm_CheckDocSpace(1: string userId, 2: i64 spaceSize) throws (1: EThriftException.ncTException exp)

    // 3.29 检查用户空间是否足够
    void Usrm_CheckUserSpace(1: string userId, 2: i64 spaceSize) throws (1: EThriftException.ncTException exp)

    // 3.30 重新计算admin限额空间
    void Usrm_ReCalcAdminLimitSpace() throws (1: EThriftException.ncTException exp)

    // 3.31 获取系统初始化状态
    bool Usrm_GetSystemInitStatus() throws (1: EThriftException.ncTException exp)

    // 3.32 初始化系统
    void Usrm_InitSystem() throws (1: EThriftException.ncTException exp)

    // 3.33 设置管控密码
    void Usrm_SetPwdControl(1: string userId, 2: ncTUsrmPwdControlConfig param) throws (1: EThriftException.ncTException exp)

    // 3.34 获取管控密码
    ncTUsrmPwdControlConfig Usrm_GetPwdControl(1: string userId) throws (1: EThriftException.ncTException exp)

    // 3.35 设置是否启用域认证或第三方认证密码锁策略
    void Usrm_SetThirdPwdLock(1: bool enable) throws (1: EThriftException.ncTException exp)

    // 3.36 获取域认证或第三方认证是否启用密码锁策略状态
    bool Usrm_GetThirdPwdLock() throws (1: EThriftException.ncTException exp)

    // 3.37 获取租户用量统计
    string Usrm_GetTenantUsageStatistics(1: string userId) throws (1: EThriftException.ncTException exp)

    // 3.38 设置用户自动禁用配置
    void Usrm_SetAutoDisable(1: ncTUserAutoDisableConfig params) throws(1: EThriftException.ncTException exp);

    // 3.39 获取用户自动禁用配置
    ncTUserAutoDisableConfig Usrm_GetAutoDisable() throws(1: EThriftException.ncTException exp);

    // 3.40 开启关闭冻结功能，True:开启，False:关闭
    void Usrm_SetFreezeStatus(1: bool status) throws(1: EThriftException.ncTException exp)

    // 3.41 获取冻结状态
    bool Usrm_GetFreezeStatus() throws(1: EThriftException.ncTException exp)

    // 3.42 冻结|解冻用户
    void Usrm_SetUserFreezeStatus(1: string userId, 2: bool freezeStatus) throws(1: EThriftException.ncTException exp)

    // 3.43 开启或关闭实名认证功能
    void Usrm_SetRealNameAuthStatus(1: bool status) throws(1: EThriftException.ncTException exp)

    // 3.44 获取实名认证开关状态（默认关闭）
    bool Usrm_GetRealNameAuthStatus() throws(1: EThriftException.ncTException exp)

    // 3.45 设置用户为已实名或未实名状态（供ASC服务端调用）
    void Usrm_SetUserRealNameAuthStatus(1: string userId, 2: bool status) throws(1: EThriftException.ncTException exp)

    // 3.46 编辑内置管理员账号
    void Usrm_EditAdminAccount(1: string adminId, 2: string account) throws (1: EThriftException.ncTException exp)

    // 3.47、根据用户第三方id获取详细信息
    ncTUsrmGetUserInfo Usrm_GetUserInfoByThirdId(1: string thirdId) throws(1: EThriftException.ncTException exp)

    // 3.48、根据用户id检查用户状态，是否启用/密码是否过期
    void Usrm_CheckUserStatus(1: string userId) throws(1: EThriftException.ncTException exp)

    // 3.49、设置用户账号有效期
    void Usrm_SetUserExpireTime(1:string userId, 2:i32 expireTime) throws(1: EThriftException.ncTException exp)

    // 3.50、获取指定站点启用用户数
    i64 Usrm_GetSiteUsedUserNum(1: string siteId) throws(1: EThriftException.ncTException exp)

    // ----------------------------------------------------------------------------
    // 四、 权责分离管理
    // ----------------------------------------------------------------------------
    // 4.1 三权分立是否开启
    bool Usrm_GetTriSystemStatus( ) throws(1: EThriftException.ncTException exp)

    // 4.2 开启关闭三权分立,True:开启，False:关闭
    void Usrm_SetTriSystemStatus(1: bool enable) throws(1: EThriftException.ncTException exp)

    // ----------------------------------------------------------------------------
    // 五、 第三方认证管理
    // ----------------------------------------------------------------------------
    // 5.1 获取第三方认证管理信息（认证类暂时限制为最多只有一个）
    ncTThirdPartyAuthConf Usrm_GetThirdPartyAuth() throws(1: EThriftException.ncTException exp)

    // 5.2 新增第三方配置
    i64 AddThirdPartyAppConfig (1: ncTThirdPartyConfig config) throws(1: EThriftException.ncTException exp)

    // 5.3 设置第三方配置
    void SetThirdPartyAppConfig (1: ncTThirdPartyConfig config) throws(1: EThriftException.ncTException exp)

    // 5.4 删除第三方配置
    void DeleteThirdPartyAppConfig (1: i64 indexId) throws (1: EThriftException.ncTException exp)

    // 5.5 获取第三方配置
    list<ncTThirdPartyConfig> GetThirdPartyAppConfig(1: ncTPluginType pluginType) throws(1: EThriftException.ncTException exp)

    // 5.6 域反向同步一次
    void SYNC_SyncToADOnce( ) throws(1: EThriftException.ncTException exp)

    // 5.7 第三方同步(如果为域同步，则appId为域id; autoSync: True-定期同步， False-单次同步)
    void SYNC_StartSync(1: string appId, 2: bool autoSync) throws(1: EThriftException.ncTException exp)

    // 5.8 增加第三方数据库信息
    string AddThirdSyncDBInfo(1: ncTThirdDBInfo thirdDbInfo) throws(1: EThriftException.ncTException exp)

    // 5.9 获取第三方数据库信息
    ncTThirdDBInfo GetThirdSyncDBInfo(1: string thirdDbId ) throws(1: EThriftException.ncTException exp)

    // 5.10 编辑第三方数据库信息
    void EditThirdSyncDBInfo(1: ncTThirdDBInfo thirdDbInfo ) throws(1: EThriftException.ncTException exp)

    // 5.11 删除第三方数据库信息
    void DeleteThirdSyncDBInfo(1: string thirdDbId ) throws(1: EThriftException.ncTException exp)

    // 5.12 获取第三方数据库表信息
    ncTThirdTableInfo GetThirdDbTableInfos(1: string thirdDbId) throws(1: EThriftException.ncTException exp)

    // 5.13 删除第三方表信息
    void DeleteThirdTableInfo(1: string thirdTableId) throws(1: EThriftException.ncTException exp)

    // 5.14 增加第三方部门表信息
    string AddThirdDepartTableInfo(1: ncTThirdDepartTableInfo thirdTableInfo) throws(1: EThriftException.ncTException exp)

    // 5.15 编辑第三方部门表信息
    void EditThirdDepartTableInfo(1: ncTThirdDepartTableInfo thirdTableInfo) throws(1: EThriftException.ncTException exp)

    // 5.16 增加第三方部门关系表信息
    string AddThirdDepartRelationTableInfo(1: ncTThirdDepartRelationTableInfo thirdTableInfo) throws(1: EThriftException.ncTException exp)

    // 5.17 编辑第三方部门关系表信息
    void EditThirdDepartRelationTableInfo(1: ncTThirdDepartRelationTableInfo thirdTableInfo) throws(1: EThriftException.ncTException exp)

    // 5.18 增加第三方用户表信息
    string AddThirdUserTableInfo(1: ncTThirdUserTableInfo thirdTableInfo) throws(1: EThriftException.ncTException exp)

    // 5.19 编辑第三方用户表信息
    void EditThirdUserTableInfo(1: ncTThirdUserTableInfo thirdTableInfo) throws(1: EThriftException.ncTException exp)

    // 5.20 增加第三方用户关系表信息
    string AddThirdUserRelationTableInfo(1: ncTThirdUserDepartRelationTableInfo thirdTableInfo) throws(1: EThriftException.ncTException exp)

    // 5.21 编辑第三方用户关系表信息
    void EditThirdUserRelationTableInfo(1: ncTThirdUserDepartRelationTableInfo thirdTableInfo) throws(1: EThriftException.ncTException exp)

    // 5.22 设置第三方数据库同步配置信息
    void SetThirdDbSyncConfig(1: string thirdDbId, 2:ncTThirdDbSyncConfig syncConfig) throws(1: EThriftException.ncTException exp)

    // 5.23 获取第三方数据库同步配置信息
    ncTThirdDbSyncConfig GetThirdDbSyncConfig(1: string thirdDbId) throws(1: EThriftException.ncTException exp)

    // 5.24 二次安全设备认证
    bool Usrm_ValidateSecurityDevice(1: string params) throws(1: EThriftException.ncTException exp)

    // 5.25 向所有节点添加第三方认证插件
    void AddGlobalThirdPartyPlugin(1: ncTThirdPartyPluginInfo pluginInfo) throws (1: EThriftException.ncTException exp)

    // 5.26 向单个节点添加第三方认证插件
    void AddLocalThirdPartyPlugin(1: ncTThirdPartyPluginInfo pluginInfo) throws (1: EThriftException.ncTException exp)

    // 5.27 向第三方推送消息
    void PushMessageToThirdParty(1: string content,
                                 2: list<string> receiverIds,
                                 3: string appId)
                                 throws (1: EThriftException.ncTException exp)

    // 5.28 使用插件推送消息
    void PushMessageByPlugin(1: string content, 2: list<string> userIds) throws (1: EThriftException.ncTException exp)

    // 5.29 是否有短信发送验证码第三方插件
    bool ThirdPartySendVcodeBySMSPluginExist() throws(1: EThriftException.ncTException exp)

    // 5.30 获取第三方认证插件是否开启
    bool GetThirdAuthTypeStatus(1: ncTMFAType authtype) throws(1: EThriftException.ncTException exp)

    // ----------------------------------------------------------------------------
    // 六、 域控管理
    // ----------------------------------------------------------------------------
    // 6.1 增加域控
    i64 Usrm_AddDomain(1: ncTUsrmDomainInfo domain) throws (1: EThriftException.ncTException exp)

    // 6.2 编辑域控
    void Usrm_EditDomain(1: ncTUsrmDomainInfo domain) throws (1: EThriftException.ncTException exp)

    // 6.3 删除域控
    void Usrm_DeleteDomain(1: i64 domainId) throws (1: EThriftException.ncTException exp)

    // 6.4 获取所有域控信息
    list<ncTUsrmDomainInfo> Usrm_GetAllDomains() throws (1: EThriftException.ncTException exp)

    // 6.5 根据域名获取域控信息
    ncTUsrmDomainInfo Usrm_GetDomainByName(1:string domainName) throws (1: EThriftException.ncTException exp)

    // 6.6 根据域id获取域控信息
    ncTUsrmDomainInfo Usrm_GetDomainById(1: i64 domainId) throws (1: EThriftException.ncTException exp)

    // 6.7 开启或者关闭域控
    void Usrm_SetDomainStatus(1: i64 domainId, 2: bool status) throws (1: EThriftException.ncTException exp)

    // 6.8 展开域控节点
    ncTUsrmDomainNode Usrm_ExpandDomainNode(1: ncTUsrmDomainInfo domain, 2: string nodePath) throws (1: EThriftException.ncTException exp)

    // 6.9 设置域同步状态,-1:域同步关闭,0：域正向同步开启，1：域反向同步开启
    void Usrm_SetDomainSyncStatus(1: i64 domainId, 2: i32 status) throws(1: EThriftException.ncTException exp)

    // 6.10 获取域同步状态
    i32 Usrm_GetDomainSyncStatus(1: i64 domainId) throws(1: EThriftException.ncTException exp)

    // 6.11 设置域配置信息
    void Usrm_SetDomainConfig(1: i64 domainId, 2:ncTUsrmDomainConfig domainConfig) throws(1: EThriftException.ncTException exp)

    // 6.12 获取域配置信息
    ncTUsrmDomainConfig Usrm_GetDomainConfig(1: i64 domainId) throws(1: EThriftException.ncTException exp)

    // 6.13 设置域关键字配置信息
    void Usrm_SetDomainKeyConfig(1: i64 domainId, 2:ncTUsrmDomainKeyConfig keyConfig) throws(1: EThriftException.ncTException exp)

    // 6.14 获取域关键字配置信息
    ncTUsrmDomainKeyConfig Usrm_GetDomainKeyConfig(1: i64 domainId) throws(1: EThriftException.ncTException exp)

    // 6.15 设置域用户自动登录状态
    void Usrm_SetADSSOStatus(1: bool status) throws(1: EThriftException.ncTException exp)

    // 6.16 获取域用户自动登录状态
    bool Usrm_GetADSSOStatus() throws(1: EThriftException.ncTException exp)

    // 6.17 检查备用域是否可用
    void Usrm_CheckFailoverDomainAvailable(1: list<ncTUsrmFailoverDomainInfo> failoverDomains) throws(1: EThriftException.ncTException exp)

    // 6.18 编辑备用域
    void Usrm_EditFailoverDomains(1: list<ncTUsrmFailoverDomainInfo> failoverDomains 2:i64 parentDomainId) throws(1: EThriftException.ncTException exp)

    // 6.29 获取备用域信息
    list<ncTUsrmFailoverDomainInfo> Usrm_GetFailoverDomains(1: i64 parentDomainId) throws(1: EThriftException.ncTException exp)


    // ----------------------------------------------------------------------------
    // 七、导入用户管理
    // ----------------------------------------------------------------------------
    // 7.1 只导入域控节点下的用户
    void Usrm_ImportDomainUsers(1: ncTUsrmImportContent content, 2: ncTUsrmImportOption option, 3: string responsiblePersonId) throws (1: EThriftException.ncTException exp)

    // 7.2 导入域控组织结构和用户
    void Usrm_ImportDomainOUs(1: ncTUsrmImportContent content, 2: ncTUsrmImportOption option, 3: string responsiblePersonId) throws (1: EThriftException.ncTException exp)

    // 7.3 获取导入进度
    ncTUsrmImportResult Usrm_GetImportProgress() throws (1: EThriftException.ncTException exp)

    // 7.4 清除导入进度
    void Usrm_ClearImportProgress() throws (1: EThriftException.ncTException exp)

    // 7.5 获取第三方根组织节点
    list<ncTThirdPartyRootNodeInfo> Usrm_GetThirdPartyRootNode(1: string userId) throws (1: EThriftException.ncTException exp)

    // 7.6 展开第三方节点
    ncTUsrmThirdPartyNode Usrm_ExpandThirdPartyNode(1: string thirdId) throws (1: EThriftException.ncTException exp)

    // 7.7 导入第三方组织结构和用户
    void Usrm_ImportThirdPartyOUs(1: list<ncTUsrmThirdPartyOU> ous, 2: list<ncTUsrmThirdPartyUser> users, 3: ncTUsrmImportOption option, 4: string responsiblePersonId) throws (1: EThriftException.ncTException exp)

    // 7.8 上传excel文件，导入
    void Usrm_ImportBatchUsers(1: ncTBatchUsersFile userInfoFile, 2: bool userCover,
                                                3: string responsiblePersonId) throws (1: EThriftException.ncTException exp)
    // 7.9 导出用户信息
    string Usrm_ExportBatchUsers(1: list<string> departmentIds, 2: string responsiblePersonId) throws (1: EThriftException.ncTException exp)

    // 7.10 下载带有用户信息的exel表
    string Usrm_DownloadBatchUsers(1: string taskId) throws (1: EThriftException.ncTException exp)

    // 7.11 下载导入失败的用户信息exel表
    string Usrm_DownloadImportFailedUsers() throws (1: EThriftException.ncTException exp)

    // 7.12 获取导入、导出进度
    ncTUsrmImportResult Usrm_GetProgress() throws (1: EThriftException.ncTException exp)

    // 7.13 获取错误信息
    list<ncTImportFailInfo> Usrm_GetErrorInfos(1:i64 start, 2:i64 limit) throws (1: EThriftException.ncTException exp)

    // 7.14 获取导出任务的状态
    bool Usrm_GetExportBatchUsersTaskStatus(1: string taskId) throws (1: EThriftException.ncTException exp)
    // ----------------------------------------------------------------------------
    // 八、联系人管理
    // ----------------------------------------------------------------------------
    // 8.1 创建联系人组
    string Usrm_CreatePersonGroup(1: string userId, 2: string groupName) throws(1: EThriftException.ncTException exp)

    // 8.2 删除联系人组
    void Usrm_DeletePersonGroup(1: string userId, 2: string groupId) throws(1: EThriftException.ncTException exp)

    // 8.3 编辑联系人组
    void Usrm_EditPersonGroup(1: string userId, 2: string groupId, 3: string newName) throws(1: EThriftException.ncTException exp)

    // 8.4 根据用户id获取所有的联系人组
    list<ncTPersonGroup> Usrm_GetPersonGroups(1: string userId) throws(1: EThriftException.ncTException exp)

    // 8.5 根据用户id批量添加用户到联系人组中
    void Usrm_AddPersonById(1: string userId, 2: list<string> userIds, 3: string groupId) throws(1: EThriftException.ncTException exp)

    // 8.6 从联系人组中批量删除用户
    void Usrm_DelPerson(1: string userId, 2: list<string> userIds, 3: string groupId) throws(1: EThriftException.ncTException exp)

    // 8.7 分页获取联系人组的用户信息
    list<ncTUsrmGetUserInfo> Usrm_GetPersonFromGroup(1: string userId, 2: string groupId, 3: i32 start, 4: i32 limit)
                                                        throws(1: EThriftException.ncTException exp)

    // 8.8 从联系人组信息中根据用户显示名搜索用户
    list<ncTSearchPersonGroup> Usrm_SearchPersonFromGroupByName(1: string userId, 2: string searchKey)
                                                        throws(1: EThriftException.ncTException exp)

    // ----------------------------------------------------------------------------
    // 九、在线人数统计管理
    // ----------------------------------------------------------------------------
    // 9.1 获取当前在线的人数统计信息
    list <ncTOpermOnlineUserInfo> Operm_GetCurrentOnlineUser() throws(1: EThriftException.ncTException exp)

    // 9.2 获取指定月份每天的最大在线数
    list <ncTOpermOnlineUserInfo> Operm_GetMaxOnlineUserDay(1: string dateMonth) throws(1: EThriftException.ncTException exp)

    // 9.3 获取月份间每天的最大在线数
    list <ncTOpermOnlineUserInfo> Operm_GetMaxOnlineUserMonth(1: string startMonth, 2: string endTMonth)
                                                              throws(1: EThriftException.ncTException exp)

    // 9.4 获取存在在线人数统计的最早时间
    string Operm_GetEarliestTime() throws(1: EThriftException.ncTException exp)

    // ----------------------------------------------------------------------------
    // 十一、OEM配置管理
    // ----------------------------------------------------------------------------
    // 11.1 设置 oem 信息
    void OEM_SetConfig(1: ncTOEMInfo oemInfo) throws (1: EThriftException.ncTException exp)

    // 11.2 根据section获取oem信息
    list<ncTOEMInfo> OEM_GetConfigBySection(1: string section) throws(1: EThriftException.ncTException exp)

    // 11.3 根据option获取oem信息
    binary OEM_GetConfigByOption(1: string section, 2: string option) throws(1: EThriftException.ncTException exp)

    // 11.4 设置pc客户端卸载口令
    void OEM_SetUninstallPwd(1: string pwd) throws (1: EThriftException.ncTException exp)

    // 11.5 获取pc客户端卸载口令
    string OEM_GetUninstallPwd() throws (1: EThriftException.ncTException exp)

    // 11.6 获取pc客户端卸载口令状态
    bool OEM_GetUninstallPwdStatus() throws (1: EThriftException.ncTException exp)

    // 11.7 检查pc客户端卸载口令是否正确
    void OEM_CheckUninstallPwd(1: string pwd) throws (1: EThriftException.ncTException exp)

    // 11.8 设置自定义配置，String
    /* 支持的参数及含义
     * exit_pwd  退出口令
     * antivirus_config 杀毒服务器配置
     * recycle_delete_delay_time_unit 系统回收站延迟删除时间计量单位
     */
    void SetCustomConfigOfString(1: string key, 2: string value) throws (1: EThriftException.ncTException exp)

    // 11.9 设置自定义配置，Int64
    /* 支持的参数及含义
     * recycle_delete_delay_time    系统回收站延迟删除时间
     */
    void SetCustomConfigOfInt64(1: string key, 2: i64 value) throws (1: EThriftException.ncTException exp)

    // 11.10 设置自定义配置，Bool
    /* 支持的参数及含义
     * enable_exit_pwd  是否启用退出口令功能, True 表示启用; False 表示不启用
     * id_card_login_status 是否启用身份证号登录, True 表示启用; False 表示不启用
     * enable_recycle_delay_delete  是否开启系统回收站, True 表示启用; False 表示不启用
     * only_share_to_user   是否只允许共享给用户, True 表示只允许共享给用户, 搜索结果过滤组织、部门、联系人组; False 表示解除该限制
     * enable_pwd_control   是否屏蔽【管控密码】界面中的 "不允许用户自主修改密码" 和 "用户密码：输入框 随机密码", True 表示不屏蔽; False 表示屏蔽
     * enable_set_delete_perm   是否允许在内链模板中设置 "删除" 权限, True 表示允许设置; False 表示屏蔽 "删除" 选项并删除原有模板中的 "删除" 权限
     * enable_set_folder_security_level 是否允许设置文件夹密级, True 表示允许设置; False 表示不允许设置
     * enable_http_link_audit  是否启用外链共享审核, True 表示启用; False表示不启用
     */
    void SetCustomConfigOfBool(1: string key, 2: bool value) throws (1: EThriftException.ncTException exp)

    // 11.11 获取自定义配置，String
    string GetCustomConfigOfString(1: string key) throws (1: EThriftException.ncTException exp)

    // 11.12 获取自定义配置，Int64
    i64 GetCustomConfigOfInt64(1: string key) throws (1: EThriftException.ncTException exp)

    // 11.13 获取自定义配置，Bool
    bool GetCustomConfigOfBool(1: string key) throws (1: EThriftException.ncTException exp)

    // ----------------------------------------------------------------------------
    // 十二、SMTP服务器管理
    // ----------------------------------------------------------------------------
    // 12.1 获得 SMTP 服务器配置
    ncTSmtpSrvConf SMTP_GetConfig() throws(1: EThriftException.ncTException exp)

    // 12.2 设置 SMTP 服务器
    void SMTP_SetConfig(1: ncTSmtpSrvConf conf) throws(1: EThriftException.ncTException exp)

    // 12.3 测试邮箱服务配置
    void SMTP_ServerTest(1: ncTSmtpSrvConf conf) throws(1: EThriftException.ncTException exp)

    // 12.4 测试邮件
    // 1:toList 收件人列表
    void SMTP_ReceiverTest(1: list<string> toList) throws(1: EThriftException.ncTException exp)

    // 12.5 设置管理员邮箱列表
    // 1:mailList 邮箱列表
    void SMTP_SetAdminMailList(1:string adminId, 2: list<string> mailList) throws(1: EThriftException.ncTException exp)

    // 12.6 获取管理员邮箱列表设置
    list<string> SMTP_GetAdminMailList(1:string adminId) throws(1: EThriftException.ncTException exp)

    // ----------------------------------------------------------------------------
    // 十三、告警管理
    // ----------------------------------------------------------------------------
    // 13.1 获得告警管理所有配置
    ncTAlarmConfig Alarm_GetConfig() throws(1: EThriftException.ncTException exp)

    // 13.2 配置通知中心
    void Alarm_SetConfig(1: ncTAlarmConfig conf) throws(1: EThriftException.ncTException exp)

    // 13.3 使用通知中心发起通知
    // notify:通知类型
    // param:通知参数json形式，可为空字符串
    void NC_SendNotify(1: string notify, 2: string param) throws(1: EThriftException.ncTException exp)

    // 13.4 保存告警邮箱设置
    // toEmailList: 告警邮箱收件人列表
    void SMTP_Alarm_SetConfig(1: list<string> toEmailList) throws(1: EThriftException.ncTException exp)

    // 13.5 获取告警邮箱设置
    list<string> SMTP_Alarm_GetConfig() throws(1: EThriftException.ncTException exp)


    // 13.4 使用smtp发送邮件
    // toEmailList:目标邮件列表
    // subject:邮件主题
    // content:邮件内容
    void SMTP_SendEmail(1: list<string> toEmailList, 2: string subject, 3: string content) throws(1: EThriftException.ncTException exp)

    // ----------------------------------------------------------------------------
    // 十四、Nginx配置管理
    // ----------------------------------------------------------------------------
    // 14.1 获取web_client的全局端口（集群对外端口）
    list<i32> GetGlobalPort () throws (1: EThriftException.ncTException exp);

    // 14.2 设置web_client的统一端口，会设置每个节点的本地端口
    list<ncTSetPortResult> SetGlobalPort (1: i32 httpPort, 2: i32 httpsPort) throws (1: EThriftException.ncTException exp);

    // 14.3 设置服务器域名地址，供内外网生成的外链地址一致
    /* 当应用访问地址（hostname）与EOSS访问地址（eoss hostname）相同时，调用该接口同时更新两个地址 */
    void SetHostName (1: string host) throws (1: EThriftException.ncTException exp);

    // 14.5 获取服务器域名地址
    string GetHostName () throws (1: EThriftException.ncTException exp);

    // 14.6 获取web_client的本地端口（单节点的web_client服务端口）
    list<i32> GetLocalPort () throws (1: EThriftException.ncTException exp);

    // 14.7 设置web_client的本地端口
    void SetLocalPort (1: i32 httpPort, 2: i32 httpsPort) throws (1: EThriftException.ncTException exp);

    // 14.8 设置全局的 EOSS http端口和https端口
    void SetGlobalEOSSPort(1:ncTEOSSPortInfo portInfo) throws (1: EThriftException.ncTException exp);

    // 14.9 获取全局的 EOSS http端口和https端口
    ncTEOSSPortInfo GetGlobalEOSSPort() throws (1: EThriftException.ncTException exp);

    // 14.10 设置本地的 EOSS http端口和https端口
    void SetLocalEOSSPort(1:ncTEOSSPortInfo portInfo) throws (1: EThriftException.ncTException exp);

    // 14.11 获取本地的 EOSS http端口和https端口
    ncTEOSSPortInfo GetLocalEOSSPort() throws (1: EThriftException.ncTException exp);

    // 14.12 设置本地的证书
    void SetLocalCert(1:string certFile, 2:string privateKey, 3:string caFile, 4:string caKey) throws (1: EThriftException.ncTException exp);

    // 14.13 上传全局的证书（保证每个节点都一样），使用用户自己的证书，需要证书和私钥
    void SetGlobalCert(1:string certFile, 2:string privateKey) throws (1: EThriftException.ncTException exp);

    // 14.14 生成全局的证书（保证每个节点都一样），证书为AnyShare自己签的
    void SetGlobalCertInternally() throws (1: EThriftException.ncTException exp);

    // 14.15 获取证书信息
    ncTCertInfo GetGlobalCertInfo() throws (1: EThriftException.ncTException exp);

    // 14.16 上传存储证书（保证每个节点都一样），使用用户自己的证书，需要证书和私钥
    void SetOssGlobalCert(1:string certFile, 2:string privateKey) throws (1: EThriftException.ncTException exp);

    // 14.17 生成存储证书（保证每个节点都一样），证书为AnyShare自己签的
    void SetOssGlobalCertInternally() throws (1: EThriftException.ncTException exp);

    // 14.18 获取存储证书信息
    ncTCertInfo GetOssGlobalCertInfo() throws (1: EThriftException.ncTException exp);

    // 14.19 设置全局节点的客户端HTTPS协议状态
    void SetGlobalClientHttpsStatus(1: bool status) throws (1: EThriftException.ncTException exp);

    // 14.21 设置全局的控制台HTTPS协议状态
    void SetGlobalConsoleHttpsStatus(1: bool status) throws (1: EThriftException.ncTException exp);

    // 14.23 获取全局的客户端HTTPS协议状态
    bool GetGlobalClientHttpsStatus() throws (1: EThriftException.ncTException exp);

    // 14.24 获取全局的控制台HTTPS协议状态
    bool GetGlobalConsoleHttpsStatus() throws (1: EThriftException.ncTException exp);

    // 14.25 获取 EACP HTTPS 端口
    i32 GetEACPHttpsPort() throws (1: EThriftException.ncTException exp);

    // 14.26 设置 EACP HTTPS 端口
    void SetEACPHttpsPort(1: i32 httpsPort) throws (1: EThriftException.ncTException exp);

    // 14.27 获取 EFAST HTTPS 端口
    i32 GetEFASTHttpsPort() throws (1: EThriftException.ncTException exp);

    // 14.28 设置 EFAST HTTPS 端口
    void SetEFASTHttpsPort(1: i32 httpsPort) throws (1: EThriftException.ncTException exp);

    // 14.29 检查当前节点上nginx是否可以使用指定端口
    bool CheckLocalPortAvavaiableForNginx(1: i32 port) throws (1: EThriftException.ncTException exp);

    // 14.30 设置存储对外访问ip
    void SetEossHostName (1: string host) throws (1: EThriftException.ncTException exp);

    // 14.31 获取存储对外访问ip
    string GetEossHostName () throws (1: EThriftException.ncTException exp);

    // ----------------------------------------------------------------------------
    // 十五、系统密级相关接口
    // ----------------------------------------------------------------------------

    // 15.1 设置系统密级
    void SetSysCSFLevel(1: i32 level) throws(1: EThriftException.ncTException exp)

    // 15.2 获取系统密级
    i32 GetSysCSFLevel() throws(1: EThriftException.ncTException exp)

    // 15.3 初始化密级枚举
    void InitCSFLevels(1: list <string> csflevels) throws(1: EThriftException.ncTException exp)

    // 15.4 获取密级枚举
    map<string, i32> GetCSFLevels() throws(1: EThriftException.ncTException exp)

    // 15.5 获取最大密级值
    i32 GetMaxCSFLevel() throws(1: EThriftException.ncTException exp)

    // ----------------------------------------------------------------------------
    // 十六、发现共享限制相关接口
    // ----------------------------------------------------------------------------

    // 16.1 设置系统发现共享状态：true--开启， false--关闭
    void Usrm_SetSystemFindShareStatus(1:bool status) throws (1: EThriftException.ncTException exp);

    // 16.2 获取系统发现共享状态：true--开启， false--关闭
    bool Usrm_GetSystemFindShareStatus() throws (1: EThriftException.ncTException exp);

    // 16.3 增加一条发现共享策略
    string Usrm_AddFindShareInfo(1:ncTFindShareInfo shareInfo) throws (1: EThriftException.ncTException exp);

    // 16.4 删除一条发现共享策略
    void Usrm_DeleteFindShareInfo(1:string sharerId) throws (1: EThriftException.ncTException exp);

    // 16.5 获取发现共享策略总数
    i64 Usrm_GetFindShareInfoCnt() throws (1: EThriftException.ncTException exp);

    // 16.6 分页获取发现共享策略信息
    list<ncTFindShareInfo> Usrm_GetFindShareInfoByPage(1: i32 start, 2: i32 limit) throws (1: EThriftException.ncTException exp);

    // 16.7 搜索发现共享限制信息
    list<ncTFindShareInfo> Usrm_SearchFindShareInfo(1: i32 start,
                                                    2: i32 limit,
                                                    3:string searchKey)
                                                    throws (1: EThriftException.ncTException exp);

    // ----------------------------------------------------------------------------
    // 十七、外链共享限制相关接口
    // ----------------------------------------------------------------------------

    // 17.1 设置系统外链共享状态：true--开启， false--关闭
    void Usrm_SetSystemLinkShareStatus(1:bool status) throws (1: EThriftException.ncTException exp);

    // 17.2 获取系统外链共享状态：true--开启， false--关闭
    bool Usrm_GetSystemLinkShareStatus() throws (1: EThriftException.ncTException exp);

    // 17.3 增加一条外链共享策略
    string Usrm_AddLinkShareInfo(1:ncTLinkShareInfo shareInfo) throws (1: EThriftException.ncTException exp);

    // 17.4 删除一条外链共享策略
    void Usrm_DeleteLinkShareInfo(1:string sharerId) throws (1: EThriftException.ncTException exp);

    // 17.5 获取外链共享策略总数
    i64 Usrm_GetLinkShareInfoCnt() throws (1: EThriftException.ncTException exp);

    // 17.6 分页获取外链共享策略信息
    list<ncTLinkShareInfo> Usrm_GetLinkShareInfoByPage(1: i32 start, 2: i32 limit) throws (1: EThriftException.ncTException exp);

    // 17.7 搜索外链共享限制信息
    list<ncTLinkShareInfo> Usrm_SearchLinkShareInfo(1: i32 start,
                                                    2: i32 limit,
                                                    3:string searchKey)
                                                    throws (1: EThriftException.ncTException exp);

    // ----------------------------------------------------------------------------
    // 十八、权限共享限制相关接口
    // ----------------------------------------------------------------------------

    // 18.1 设置系统权限共享状态：true--开启， false--关闭
    void Usrm_SetSystemPermShareStatus(1:bool status) throws (1: EThriftException.ncTException exp);

    // 18.2 获取系统权限共享状态：true--开启， false--关闭
    bool Usrm_GetSystemPermShareStatus() throws (1: EThriftException.ncTException exp);

    // 18.3 增加一条权限共享范围信息
    string Usrm_AddPermShareInfo(1:ncTPermShareInfo shareInfo) throws (1: EThriftException.ncTException exp);

    // 18.4 编辑一条权限共享范围信息
    void Usrm_EditPermShareInfo(1:ncTPermShareInfo shareInfo) throws (1: EThriftException.ncTException exp);

    // 18.5 删除一条权限共享范围信息
    void Usrm_DeletePermShareInfo(1:string strategyId) throws (1: EThriftException.ncTException exp);

    // 18.6 启用|禁用
    void Usrm_SetPermShareInfoStatus(1:string strategyId, 2:bool status) throws (1: EThriftException.ncTException exp);

    // 18.7 获取权限共享范围信息总数
    i64 Usrm_GetPermShareInfoCnt() throws (1: EThriftException.ncTException exp);

    // 18.8 分页获取权限共享范围信息
    list<ncTPermShareInfo> Usrm_GetPermShareInfoByPage(1: i32 start, 2: i32 limit) throws (1: EThriftException.ncTException exp);

    // 18.9 搜索权限共享范围信息
    list<ncTPermShareInfo> Usrm_SearchPermShareInfo(1: i32 start,
                                                    2: i32 limit,
                                                    3:string searchKey)
                                                    throws (1: EThriftException.ncTException exp);

    // 18.10 是否叠加默认策略
    bool Usrm_GetDefaulStrategySuperimStatus() throws (1: EThriftException.ncTException exp);

    // 18.11 设置是否叠加默认策略
    void Usrm_SetDefaulStrategySuperimStatus(1: bool status) throws (1: EThriftException.ncTException exp);

    // ----------------------------------------------------------------------------
    // 十九、防泄密权限管理
    // ----------------------------------------------------------------------------

    // 19.1 设置系统防泄密状态：true--开启， false--关闭
    void SetLeakProofStatus(1:bool status) throws (1: EThriftException.ncTException exp);

    // 19.2 获取系统防泄密状态：true--开启， false--关闭
    bool GetLeakProofStatus() throws (1: EThriftException.ncTException exp);

    // 19.3 增加一条防泄密策略，返回生成的策略id
    i64 AddLeakProofStrategy(1:ncTAddLeakProofStrategyParam param) throws (1:EThriftException.ncTException exp);

    // 19.4 编辑防泄密策略
    void EditLeakProofStrategy(1:ncTEditLeakProofStrategyParam param) throws (1:EThriftException.ncTException exp);

    // 19.5 删除单条防泄密策略
    void DeleteLeakProofStrategy(1:i64 strategyId) throws (1:EThriftException.ncTException exp);

    // 19.6 获取防泄密策略总条数
    i64 GetLeakProofStrategyCount() throws (1:EThriftException.ncTException exp);

    // 19.7 分页获取防泄密策略信息
    list<ncTLeakProofStrategyInfo> GetLeakProofStrategyInfosByPage(1:i32 start, 2:i32 limit) throws (1:EThriftException.ncTException exp);

    // 19.8 获取搜索防泄密策略信息的总条数（根据用户显示名，部门显示名）
    i64 SearchLeakProofStrategyCount(1:string key) throws (1:EThriftException.ncTException exp);

    // 19.9 搜索防泄密策略信息（根据用户显示名，部门显示名）
    list<ncTLeakProofStrategyInfo> SearchLeakProofStrategyInfosByPage(1:string key,
                                                                      2:i32 start,
                                                                      3:i32 limit)
                                                                      throws (1:EThriftException.ncTException exp);

    // ----------------------------------------------------------------------------
    // 二十、认证接口
    // ----------------------------------------------------------------------------
    // 20.1 用户登录webclient
    string Usrm_UserLogin(1: string userName, 2: string newPassword, 3: ncTUserLoginOption option)
                            throws (1: EThriftException.ncTException exp)

    // 20.1 用户登录webclient（根据NTLMV1算法）
    ncTNTLMResponse Usrm_UserLoginByNTLMV1(1: string account, 2: string challenge, 3: string password)
                            throws (1: EThriftException.ncTException exp)

    // （根据NTLMV2算法）
    ncTNTLMResponse Usrm_UserLoginByNTLMV2(1: string account, 2: string domain, 3: string challenge, 4: string password)
                            throws (1: EThriftException.ncTException exp)

    // 20.2 登录（支持webconsole|webclient），如果登录控制台失败，记录日志
    string Usrm_Login(1: string userName, 2: string password, 3: ncTUsrmAuthenType authenType, 4: ncTUserLoginOption option, 5: string osType)
                      throws(1: EThriftException.ncTException exp)

    // 20.3 向第三方认证平台验证，如果成功，返回对应的account
    string Usrm_ValidateThirdParty(1: string params) throws(1: EThriftException.ncTException exp)

    // 20.4 第三方单点登录控制台
    string Usrm_LoginConsoleByThirdParty(1: string params) throws(1: EThriftException.ncTException exp)

    // 20.5 根据用户userid与tokenid登录webconsole
    void Usrm_LoginConsoleByTokenId(1: string userId, 2: string tokenId, 3: ncTUserLoginOption option) throws(1: EThriftException.ncTException exp)

    // 20.6 获取用户登录webclient的tokenid
    string Usrm_GetLoginClientInfo(1: string userId) throws(1: EThriftException.ncTException exp)

    // 20.7 设置登录验证码配置
    void Usrm_SetVcodeConfig (1: ncTVcodeConfig vcodeconfig) throws (1:EThriftException.ncTException exp)

    // 20.8 获取登录验证码配置信息
    ncTVcodeConfig Usrm_GetVcodeConfig () throws (1:EThriftException.ncTException exp)

    // 20.9 验证码生成函数接口
    ncTVcodeCreateInfo Usrm_CreateVcodeInfo (1: string uuidIn, 2: ncTVcodeType vcodeType) throws (1: EThriftException.ncTException exp)

    // 20.10 双因子认证短信验证码发送接口
    ncTReturnInfo Usrm_SendAuthVcode (1: string userId, 2: ncTVcodeType vcodeType, 3:string oldTelnum) throws (1: EThriftException.ncTException exp)

    // 20.11 通用第三方单点登录控制台
    string Usrm_LoginConsoleByThirdPartyNew(1: string params) throws(1: EThriftException.ncTException exp)

    // 20.12 验证控制台管理员的密码
    string Usrm_CheckConsoleUserPassword(1: string userName, 2: string password, 3: ncTUsrmAuthenType authenType, 4: ncTUserLoginOption option)
                                         throws(1: EThriftException.ncTException exp)

    // ----------------------------------------------------------------------------
    // 二十一、缓存清除配置
    // ----------------------------------------------------------------------------
    // 21.1 获取清除缓存的时间间隔, -1: 未开启，
    i32 GetClearCacheInterval( ) throws (1: EThriftException.ncTException exp);

    // 21.2 设置清除缓存的时间间隔， -1: 未开启，
    void SetClearCacheInterval(1: i32 interval) throws (1: EThriftException.ncTException exp);

    // 21.3 获取清除缓存的空间限额，-1: 未开启，
    i64 GetClearCacheQuota() throws (1: EThriftException.ncTException exp);

    // 21.4 设置清除缓存的时间间隔，-1: 未开启，
    void SetClearCacheQuota(1: i64 size) throws (1: EThriftException.ncTException exp);

    // 21.5 设置客户端是否强制清除缓存
    void SetForceClearCacheStatus(1: bool status) throws (1: EThriftException.ncTException exp);

    // 21.6 获取客户端是否强制清除缓存状态
    bool GetForceClearCacheStatus() throws (1: EThriftException.ncTException exp);

    // 21.5 设置客户端是否隐藏缓存设置的状态
    void SetHideClientCacheSettingStatus(1: bool status) throws (1: EThriftException.ncTException exp);

    // 21.6 获取客户端是否隐藏缓存设置的状态
    bool GetHideClientCacheSettingStatus() throws (1: EThriftException.ncTException exp);

    // ----------------------------------------------------------------------------
    // 二十二、登录策略管理
    // ----------------------------------------------------------------------------

    // 22.1 设置登录策略状态，true--开启，false--关闭
    void SetLoginStrategyStatus(1:bool status) throws (1: EThriftException.ncTException exp);

    // 22.2 获取登录策略状态，true--开启，false--关闭
    bool GetLoginStrategyStatus() throws (1: EThriftException.ncTException exp);

    // 22.3 获取单个指定设备类型禁止登录状态
    bool GetOSTypeForbidLoginStatus(1:ncTDeviceOsType loginOSType) throws (1: EThriftException.ncTException exp);

    // 22.4 批量设置指定设备类型禁止登录状态
    void SetBatchOSTypeForbidLoginInfo(1:list<ncTOSTypeForbidLoginInfo> info) throws (1: EThriftException.ncTException exp);

    // 22.5 获取所有设备类型禁止登录状态信息
    list<ncTOSTypeForbidLoginInfo> GetAllOSTypeForbidLoginInfo() throws (1: EThriftException.ncTException exp);

    // ----------------------------------------------------------------------------
    //二十三、 客户端升级包相关接口
    // ----------------------------------------------------------------------------

    //23.1 上传客户端升级包
    void UploadClientUpdatePackage(1:string packagePath) throws (1:EThriftException.ncTException exp);

    //23.2 删除客户端升级包
    void DeleteClientUpdatePackage(1:i16 osType) throws (1:EThriftException.ncTException exp);

    //23.3 获取客户端升级包信息
    list<ncTClientPackageInfo> GetClientUpdatePackage() throws (1:EThriftException.ncTException exp);

    //23.4 获取客户端升级包下载链接
    string GetClientUpdatePackageURL(1:i16 osType, 2: string reqHost, 3: bool useHttps) throws (1:EThriftException.ncTException exp);

    //23.5 获取客户端升级包信息
    ncTClientPackageInfo GetClientUpdatePackageInfo(1:i32 osType) throws (1:EThriftException.ncTException exp);

    //23.6 编辑客户端升级包模式
    void EditClientUpdatePackageMode(1:i32 osType, 2:bool mode) throws (1:EThriftException.ncTException exp);

    //23.7 设置客户端升级包下载信息
    void SetClientUpdatePackageDownloadInfo(1:string name, 2:string url) throws (1:EThriftException.ncTException exp);

    // ----------------------------------------------------------------------------
    //二十四、 多租户管理
    // ----------------------------------------------------------------------------
    // 24.1 设置多租户开启状态
    void SetMultiTenantStatus(1: bool status) throws (1: EThriftException.ncTException exp);

    // 24.2 获取多租户开启状态
    bool GetMultiTenantStatus() throws (1: EThriftException.ncTException exp);

    // --------------------------------------
    //二十五、 提供给openapi使用
    // --------------------------------------
    // 25.1 添加第三方用户appid
    string Usrm_AddThirdApp(1:string apppid) throws (1: EThriftException.ncTException exp);

    // 25.2 设置第三方用户状态
    void Usrm_SetThirdAppStatus(1:string appid, 2:bool status) throws (1: EThriftException.ncTException exp);

    // 25.3 生成签名
    string Usrm_GenThirdAppSign(1:string appid, 2:string appkey, 3:string method, 4: string body) throws (1: EThriftException.ncTException exp);

    // 25.4 检查签名
    void Usrm_CheckThirdAppSign(1:string appid, 2:string method, 3:string body, 4:string sign) throws (1: EThriftException.ncTException exp);

    // --------------------------------------
    //二十六、 共享审核策略配置管理
    // --------------------------------------
    // 26.1 设置审核机制状态
    void Auditm_SetPolicyStatus(1: bool status) throws(1: EThriftException.ncTException exp);

    // 26.2 获取审核机制状态
    bool Auditm_GetPolicyStatus() throws(1: EThriftException.ncTException exp);

    // 26.3 根据操作者id和文档对象id获取对应的审核员ids
    list<string> Auditm_GetAuditorIds(1:string docId, 2:ncTAuditType type) throws(1: EThriftException.ncTException exp);

    // 26.4 判断是否是审核员
    bool Auditm_IsAuditor(1:string userId) throws(1: EThriftException.ncTException exp);

    // 26.5 添加部门到免审核清单
    void AuditWhiteListm_AddDepartments(1: list<string> departIds) throws (1: EThriftException.ncTException exp);

    // 26.6 从免审核清单中搜索部门
    list<ncTAuditWhiteListItem> AuditWhiteListm_Search(1: i32 start, 2: i32 limit, 3: string searchKey) throws (1: EThriftException.ncTException exp);

    // 26.7 搜索条目
    i32 AuditWhiteListm_SearchCount(1: string searchKey) throws (1: EThriftException.ncTException exp);

    // 26.8 从免审核清单中获取部门
    list<ncTAuditWhiteListItem> AuditWhiteListm_GetInfosByPage(1: i32 start, 2: i32 limit) throws (1: EThriftException.ncTException exp);

    // 26.9 获取条目
    i32 AuditWhiteListm_GetInfosCount() throws (1: EThriftException.ncTException exp);

    // 26.10 从免审核清单中删除部门
    void AuditWhiteListm_DelDepartment(1: string departmentId) throws (1: EThriftException.ncTException exp);

    // 26.11 设置免审核文件密级
    void AuditWhiteListm_SetCSFLevel(1: i32 level) throws (1: EThriftException.ncTException exp);

    // 26.12 获取免审核文件密级
    i32 AuditWhiteListm_GetCSFLevel() throws (1: EThriftException.ncTException exp);

    // 26.13 设置部门状态
    void AuditWhiteListm_SetDepartmentStatus(1: string departmentId, 2: bool status) throws (1: EThriftException.ncTException exp);

    // 26.14 检查部门是否免审核
    bool AuditWhiteListm_CheckAuditFree(1: list<string> departIds) throws (1: EThriftException.ncTException exp);

    // 26.15 获取部门状态
    bool AuditWhiteListm_GetDepartmentStatus(1: string departId) throws (1: EThriftException.ncTException exp);

    // ----------------------------------------------------------------------------
    //二十七、 第三方预览工具管理
    // ----------------------------------------------------------------------------
    // 27.1 获取第三方预览工具配置信息
    ncTThirdPartyToolConfig GetThirdPartyToolConfig(1: string thirdPartyToolId) throws (1: EThriftException.ncTException exp);

    // 27.2 设置第三方预览工具配置信息
    void SetThirdPartyToolConfig(1: ncTThirdPartyToolConfig thirdPartyToolConfig) throws (1: EThriftException.ncTException exp);

    // 27.3 测试第三方预览工具配置信息
    bool TestThirdPartyToolConfig(1:string url) throws (1: EThriftException.ncTException exp);

    // 27.4 获取AnyRobot跳转URL
    string GetAnyRobotURL(1: string host, 2: string account) throws (1: EThriftException.ncTException exp);

    // 27.5 获取站点 sitename 第三方配置信息(Office, WOPI url)
    string GetSiteOfficeOnlineInfo(1: string siteName) throws (1: EThriftException.ncTException exp);

    // 27.6 设置站点 sitename 第三方配置信息(Office, WOPI url)
    void SetSiteOfficeOnlineInfo(1: string siteName, 2: string info) throws (1: EThriftException.ncTException exp);

    // ----------------------------------------------------------------------------
    // 二十九、用户登录访问控制管理
    // ----------------------------------------------------------------------------
    // 29.1：添加用户网段设置
    void Usrm_AddNetAccessorsInfo(1:ncTNetAccessorsInfo netAccessorsInfo) throws (1: EThriftException.ncTException exp);

    // 29.2 编辑用户网段设置
    void Usrm_EditNetAccessorsInfo(1:ncTNetAccessorsInfo netAccessorsInfo) throws (1: EThriftException.ncTException exp);

    // 29.3 删除用户网段设置
    void Usrm_DeleteNetAccessorsInfo(1:string netAccessorsId) throws (1: EThriftException.ncTException exp);

    // 29.4 获取网段设置
    list<ncTNetAccessorsInfo> Usrm_GetNet() throws (1: EThriftException.ncTException exp);

    // 29.5 根据ip搜索网段设置
    list<ncTNetAccessorsInfo> Usrm_SearchNet(1:string ip) throws (1: EThriftException.ncTException exp);

    // 29.6 在指定网段设置中获取所有访问者
    list<ncTAccessorInfo> Usrm_GetAccessors(1:string netAccessorsId) throws (1: EThriftException.ncTException exp);

    // 29.7 在指定网段设置中搜索某个访问者
    list<ncTAccessorInfo> Usrm_SearchAccessors(1:string netAccessorsId, 2:string name) throws (1: EThriftException.ncTException exp);

    // 29.8 搜索指定访问者的登录绑定信息
    ncTUserLoginAccessControl Usrm_SearchLoginAccessControlByName(1:string name) throws (1: EThriftException.ncTException exp);

    // 29.9 检查指定访问者ip是否允许登录访问
    bool Usrm_CheckLoginIp(1:string userId, 2:string loginIp) throws (1: EThriftException.ncTException exp);

    // 29.10 设置标签页[优先访问设置]显示状态
    void Usrm_SetPriorityAccessTabStatus(1:bool stauts) throws (1:EThriftException.ncTException exp);

    // 29.11 获取标签页[优先访问设置]显示状态
    bool Usrm_GetPriorityAccessTabStatus() throws (1:EThriftException.ncTException exp);

    // 29.12 设置优先访问配置信息
    void Usrm_SetPriorityAccessConfig(1:ncTPriorityAccessConfig config) throws (1:EThriftException.ncTException exp);

    // 29.13 获取优先访问配置信息
    ncTPriorityAccessConfig Usrm_GetPriorityAccessConfig() throws (1:EThriftException.ncTException exp);

    // 29.14 更新本地优先访问开关缓存状态
    void Usrm_SetPriorityAccessLocalCacheStatus(1:bool status) throws (1:EThriftException.ncTException exp);

    // ----------------------------------------------------------------------------
    // 三十、文档审核流程控制
    // ----------------------------------------------------------------------------
    // 30.1 创建审核流程，返回流程唯一标识id
    string DocAuditm_CreateProcess(1:ncTDocAuditInfo docAuditInfo) throws (1: EThriftException.ncTException exp);

    // 30.2 编辑审核流程
    void DocAuditm_EditProcess(1:ncTDocAuditInfo editParam, 2: string editorId) throws (1: EThriftException.ncTException exp);

    // 30.3 删除审核流程
    void DocAuditm_DeleteProcess(1:string processId) throws (1: EThriftException.ncTException exp);

    // 30.4 根据管理员id获取所有文档流程信息, admin获取所有
    list<ncTDocAuditInfo> DocAuditm_GetAllProcessInfo(1: string userId) throws (1: EThriftException.ncTException exp);

    // 30.5 根据审核流程名搜索审核流程
    list<ncTDocAuditInfo> DocAuditm_SearchProcessInfoByName(1: string userId, 2: string searchKey) throws (1: EThriftException.ncTException exp);

    // 30.6 获取所有文档审核员信息
    list<ncTSimpleUserInfo> DocAuditm_GetAllAuditorInfos(1: string userId) throws (1: EThriftException.ncTException exp);

    // 30.7 搜索文档审核员信息
    list<ncTSimpleUserInfo> DocAuditm_SearchAuditor(1: string userId, 2: string name) throws (1: EThriftException.ncTException exp);

    // 30.8 根据流程id获取审核流程信息
    ncTDocAuditInfo DocAuditm_GetProcessById(1:string processId) throws (1: EThriftException.ncTException exp);

    // 30.9 转换文档名称
    string DocAuditm_ConvertDocName(1:string gns) throws (1: EThriftException.ncTException exp);

    // 30.10 根据普通用户id获取所能访问的文档流程信息
    list<ncTDocAuditInfo> DocAuditm_GetScopedProcessInfo(1: string userId) throws (1: EThriftException.ncTException exp);

    // 30.11 检查流程对于用户是否可见
    bool DocAuditm_CheckProcessScope(1: string userId, 2:string processId) throws (1: EThriftException.ncTException exp);

    // ----------------------------------------------------------------------------
    // 三十一、处理集成到anyshare的外部应用
    // ----------------------------------------------------------------------------
    // 31.1 跳转登录到外部应用中
    string ExtApp_GetInfo(1: string params, 2: string userId) throws(1: EThriftException.ncTException exp)

    // ----------------------------------------------------------------------------
    // 三十二、涉密模块处理
    // ----------------------------------------------------------------------------
    // 32.1 涉密总开关
    bool Secretm_GetStatus() throws(1: EThriftException.ncTException exp)

    // ----------------------------------------------------------------------------
    // 三十三、跨网段数据交换
    // ----------------------------------------------------------------------------
    // 33.1 启用或关闭内外网数据交换
    void DocExchangem_SetStatus(1: bool status) throws(1: EThriftException.ncTException exp);

    // 33.2 内外网数据交换是否开启
    bool DocExchangem_GetStatus() throws(1: EThriftException.ncTException exp);

    // 33.3 获取当前站点密钥
    string DocExchangem_GetSendKey() throws(1: EThriftException.ncTException exp);

    // 33.4 重置当前站点密钥
    string DocExchangem_SetSendKey() throws(1: EThriftException.ncTException exp);

    // 33.5 跨网段数据交换是否需要审核
    bool DocExchangem_GetAuditStatus() throws(1: EThriftException.ncTException exp);

    // 33.6 设置跨网段数据交换是否需要审核
    void DocExchangem_SetAuditStatus(1: bool status) throws(1: EThriftException.ncTException exp);

    // 33.7 启用或关闭限制跨网段交换的文档范围
    void DocExchangem_SetLimitStatus(1: bool status) throws(1: EThriftException.ncTException exp);

    // 33.8 是否启用限制跨网段交换的文档范围
    bool DocExchangem_GetLimitStatus() throws(1: EThriftException.ncTException exp);

    // 33.9 添加可共享的文档范围信息
    void DocExchangem_Set(1: list<ncTDocExchangeInfo> params, 2: ncTDocExchangeLimitType limitType) throws(1: EThriftException.ncTException exp);

    // 33.10 分页获取可共享的文档范围信息
    list<ncTDocExchangeInfo> DocExchangem_Get(1: i32 start, 2: i32 limit, 3: ncTDocExchangeLimitType limitType) throws(1: EThriftException.ncTException exp);

    // 33.11 获取数目
    i32 DocExchangem_GetCnts(1: ncTDocExchangeLimitType limitType) throws(1: EThriftException.ncTException exp);

    // 33.12 分页搜索
    list<ncTDocExchangeInfo> DocExchangem_Search(1: i32 start, 2: i32 limit, 3: string searchKey, 4: ncTDocExchangeLimitType limitType) throws(1: EThriftException.ncTException exp);

    // 33.13 搜索数目
    i32 DocExchangem_SearchCnts(1: string searchKey, 2: ncTDocExchangeLimitType limitType) throws(1: EThriftException.ncTException exp);

    // 33.14 删除
    void DocExchangem_Delete(1: string objId, 2: ncTDocExchangeLimitType limitType) throws(1: EThriftException.ncTException exp);

    // 33.15 检查对象是否允许发起内外网数据交换/指定文档库同步的范围内
    bool DocExchangem_CheckLimitScope(1: string objId, 2: ncTDocExchangeLimitType limitType) throws(1: EThriftException.ncTException exp);

    // 33.15 注册内外网数据交换服务节点
    void DocExchangem_RegisterService() throws(1: EThriftException.ncTException exp);

    // 33.16 获取内外网数据交换服务节点ip
    string DocExchangem_GetServiceIp() throws(1: EThriftException.ncTException exp);

    // 33.17 设置内外网组织同步相关配置
    void DocExchangem_SetSyncOuConfig(1: bool isEnable, 2: i32 intervalTime) throws(1: EThriftException.ncTException exp);

    // 33.18 获取自动交换状态
    bool DocExchangem_GetAutoStatus() throws(1: EThriftException.ncTException exp);

    // 33.19 设置自动交换状态
    void DocExchangem_SetAutoStatus(1: bool status) throws(1: EThriftException.ncTException exp);

    // 33.20 获取自动删除发件箱内文件状态
    bool DocExchangem_GetDelFileStatus() throws(1: EThriftException.ncTException exp);

    // 33.21 设置自动删除发件箱内文件状态
    void DocExchangem_SetDelFileStatus(1: bool status) throws(1: EThriftException.ncTException exp);

    // 33.22 获取文档库内外网同步状态
    bool DocExchangem_GetLibSyncStatus() throws(1: EThriftException.ncTException exp);

    // 33.23 设置文档库内外网同步状态
    void DocExchangem_SetLibSyncStatus(1: bool status) throws(1: EThriftException.ncTException exp);

    // 33.24 文档交换加密是否开启，默认true
    bool DocExchangem_GetEncryptStatus() throws(1: EThriftException.ncTException exp);

    // 33.25 开启或关闭文档交换加密
    void DocExchangem_SetEncryptStatus(1: bool status) throws(1: EThriftException.ncTException exp);

    // 33.26 是否根据来源自动存放接收文档，默认false
    bool DocExchangem_GetAutoRecvStatus() throws(1: EThriftException.ncTException exp);

    // 33.27 开启或关闭根据来源自动存放接收文档
    void DocExchangem_SetAutoRecvStatus(1: bool status) throws(1: EThriftException.ncTException exp);

    // 33.28 添加接收区
    string DocExchangem_AddRecvArea(1: ncTDocExchangeRecvArea param) throws(1: EThriftException.ncTException exp);

    // 33.29 获取接收区信息
    list<ncTDocExchangeRecvArea> DocExchangem_GetRecvAreas() throws(1: EThriftException.ncTException exp);

    // 33.30 删除接收区
    void DocExchangem_DeleteRecvArea(1: string recvAreaId) throws(1: EThriftException.ncTException exp);

    // 33.31 修改接收区
    void DocExchangem_ModifyRecvArea(1: ncTDocExchangeRecvArea param) throws(1: EThriftException.ncTException exp);

    // 33.32 导出文档库名
    string DocExchangem_ExportDocName() throws(1: EThriftException.ncTException exp);

    // 33.33 导入接收区文档库名
    /**
     * @param recvAreaId: 接收区ID
     * @param importInfo: 导入操作相关信息，若为用户上传文件，则为文件名
     * @param content: 导入数据，若为用户上传文件，则为文件内容
     * @throw: 转抛内部调用异常
     */
    void DocExchangem_ImportRecvAreaDocName(1: string recvAreaId, 2: string importInfo, 3: string content) throws(1: EThriftException.ncTException exp);

    // 33.34 删除接收区文档库名
    void DocExchangem_DelRecvAreaDocName(1: string recvAreaId) throws(1: EThriftException.ncTException exp);

    // 33.35 获取手动发起交换时是否发送到收件箱状态
    bool DocExchangem_GetManualToInboxStatus() throws(1: EThriftException.ncTException exp);

    // 33.36 设置手动发起交换时是否发送到收件箱状态
    void DocExchangem_SetManualToInboxStatus(1: bool status) throws(1: EThriftException.ncTException exp);

    // 33.37 启用或关闭限制文档库内外网同步的文档范围
    void DocExchangem_SetLibSyncLimitStatus(1: bool status) throws(1: EThriftException.ncTException exp);

    // 33.38 是否启用限制文档库内外网同步的文档范围
    bool DocExchangem_GetLibSyncLimitStatus() throws(1: EThriftException.ncTException exp);

    // ----------------------------------------------------------------------------
    // 三十四、NAS服务配置管理
    // ----------------------------------------------------------------------------
    // 34.1 激活当前节点NAS网关服务
    void NAS_Active() throws(1: EThriftException.ncTException exp)

    // 34.2 卸载当前结点NAS网关服务
    void NAS_Deactive() throws(1: EThriftException.ncTException exp)

    // 34.3 获取当前已激活NAS服务的节点 ip list
    list<string> NAS_GetNodeList() throws(1: EThriftException.ncTException exp)

    // 34.4 列取挂载路径
    list<ncTNASMountInfo> NAS_ListMountPoints() throws(1: EThriftException.ncTException exp)

    // 34.5 添加挂载路径
    void NAS_AddMountPoint(1: string MountName, 2: string path) throws(1: EThriftException.ncTException exp)

    // 34.6 删除挂载路径
    void NAS_DelMountPoint(1: string MountName) throws(1: EThriftException.ncTException exp)

    // 34.7 检查集群中nas服务状态  当有一个或以上的节点提供服务时，返回true
    bool NAS_CheckService() throws(1: EThriftException.ncTException exp)

    // 34.8 添加当前节点挂载路径 （不对外使用）
    void NAS_LocalAddMountPoint(1: string MountName, 2: string path) throws(1: EThriftException.ncTException exp)

    // 34.9 删除当前节点挂载路径 （不对外使用）
    void NAS_LocalDelMountPoint(1: string MountName) throws(1: EThriftException.ncTException exp)

    // 34.10 删除许可证时卸载一个NAS节点 （不对外使用）
    void NAS_OnDelLincense() throws(1: EThriftException.ncTException exp)

    // ----------------------------------------------------------------------------
    // 三十五、共享邀请管理
    // ----------------------------------------------------------------------------
    // 35.1 设置系统共享邀请状态：true--开启， false--关闭
    void Usrm_SetSystemInvitationShareStatus(1:bool status) throws (1: EThriftException.ncTException exp);

    // 35.2 获取系统共享邀请状态：true--开启， false--关闭
    bool Usrm_GetSystemInvitationShareStatus() throws (1: EThriftException.ncTException exp);

    // ----------------------------------------------------------------------------
    // 三十六、限速配置管理
    // ----------------------------------------------------------------------------
    // 36.1 增加一条限速信息
    string Usrm_AddLimitRateInfo(1: ncTLimitRateInfo info) throws (1: EThriftException.ncTException exp);

    // 36.2 编辑一条限速信息
    void Usrm_EditLimitRateInfo(1: ncTLimitRateInfo info) throws (1: EThriftException.ncTException exp);

    // 36.3 删除一条限速信息
    void Usrm_DeleteLimitRateInfo(1: string id, 2: ncTLimitRateType limitType) throws (1: EThriftException.ncTException exp);

    // 36.4 获取限速信息总数
    i64 Usrm_GetLimitRateInfoCnt(1: ncTLimitRateType limitType) throws (1: EThriftException.ncTException exp);

    // 36.5 分页获取限速信息
    list<ncTLimitRateInfo> Usrm_GetLimitRateInfoByPage(1: i32 start, 2: i32 limit, 3: ncTLimitRateType limitType) throws (1: EThriftException.ncTException exp);

    // 36.6 搜索限速信息
    list<ncTLimitRateInfo> Usrm_SearchLimitRateInfoByPage(1: string searchKey, 2: i32 start, 3: i32 limit, 4: ncTLimitRateType limitType) throws (1: EThriftException.ncTException exp);

    // 36.7 搜索限速信息总数
    i64 Usrm_SearchLimitRateInfoCnt(1: string searchKey, 2: ncTLimitRateType limitType) throws (1: EThriftException.ncTException exp);

    // 36.8. 设置限速配置开关状态
    void Usrm_SetLimitRateConfig(1: ncTLimitRateConfig conf) throws(1: EThriftException.ncTException exp);

    // 36.9. 获取限速配置开关状态
    ncTLimitRateConfig Usrm_GetLimitRateConfig() throws(1: EThriftException.ncTException exp);

    // 36.10. 获取已存在其他限速规则的对象信息
    ncTLimitRateObjInfo Usrm_GetExistObjectInfo(1: list<ncTLimitRateObject> userInfos, 2: list<ncTLimitRateObject> depInfos,
                                                 3: ncTLimitRateType limitType, 4: string limitId) throws (1: EThriftException.ncTException exp);

    // ----------------------------------------------------------------------------
    // 三十七、第三方标密系统配置
    // ----------------------------------------------------------------------------
    // 37.1 设置第三方标密系统配置
    void SetThirdCSFSysConfig(1: ncTThirdCSFSysConfig config) throws (1: EThriftException.ncTException exp);

    // 37.2 获取第三方标密系统配置
    ncTThirdCSFSysConfig GetThirdCSFSysConfig() throws (1: EThriftException.ncTException exp);

    // ----------------------------------------------------------------------------
    // 三十八、文件水印策略配置
    // ----------------------------------------------------------------------------
    // 38.1 获取文件水印策略配置
    string GetDocWatermarkConfig() throws (1: EThriftException.ncTException exp)

    // 38.2 设置文件水印策略配置
    void SetDocWatermarkConfig(1: string config) throws (1: EThriftException.ncTException exp);

    // 38.3 添加开启下载水印的文档库
    void AddWatermarkDoc(1:string id, 2: i32 watermarkType) throws (1: EThriftException.ncTException exp);

    // 38.4 更新开启下载水印的文档库
    void UpdateWatermarkDoc(1:string id, 2: i32 watermarkType) throws (1: EThriftException.ncTException exp);

    // 38.5 获取所有开启下载水印的文档库
    list<ncTWatermarkDocInfo> GetWatermarkDocs() throws (1: EThriftException.ncTException exp)

    // 38.6 删除开启下载水印的文档库
    void DeleteWatermarkDoc(1:string id) throws (1: EThriftException.ncTException exp);

    // 38.7 获取开启下载水印的文档库总数
    i64 GetWatermarkDocCnt() throws (1: EThriftException.ncTException exp);

    // 38.8 分页获取开启下载水印的文档库信息
    list<ncTWatermarkDocInfo> GetWatermarkDocByPage(1: i32 start, 2: i32 limit) throws (1: EThriftException.ncTException exp);

    // 38.9 搜索开启下载水印的文档库总数
    i64 SearchWatermarkDocCnt(1:string searchKey) throws (1: EThriftException.ncTException exp);

    // 38.10 搜索开启下载水印的文档库信息
    list<ncTWatermarkDocInfo> SearchWatermarkDocByPage(1:string searchKey, 2: i32 start, 3: i32 limit) throws (1: EThriftException.ncTException exp);

    // ----------------------------------------------------------------------------
    // 三十九、内外链共享模板策略
    // ----------------------------------------------------------------------------
    // 39.1 添加模板
    list<string> AddLinkTemplate(1: ncTLinkTemplateInfo templateInfo) throws (1: EThriftException.ncTException exp);

    // 39.2 删除模板
    void DeleteLinkTemplate(1: string templateId) throws (1: EThriftException.ncTException exp);

    // 39.3 编辑模板
    list<string> EditLinkTemplate(1: ncTLinkTemplateInfo templateInfo) throws (1: EThriftException.ncTException exp);

    // 39.4 获取模板
    list<ncTLinkTemplateInfo> GetLinkTemplate(1: i32 templateType) throws (1: EThriftException.ncTException exp);

    // 39.5 搜索模板
    list<ncTLinkTemplateInfo> SearchLinkTemplate(1: i32 templateType, 2: string key) throws (1: EThriftException.ncTException exp);

    // 39.6 根据用户ID获取生效的模板
    ncTLinkTemplateInfo GetCalculatedLinkTemplateBySharerId(1: i32 templateType, 2: string userId) throws (1: EThriftException.ncTException exp);

    // 39.8 检查外链共享权限是否符合模板
    void CheckExternalLinkPerm(1: ncTExternalLinkInfo linkInfo) throws (1: EThriftException.ncTException exp);

    // ----------------------------------------------------------------------------
    // 四十、网段文档库绑定管理
    // ----------------------------------------------------------------------------
    // 40.1 设置网段文档库绑定开关状态
    void DocLimitm_SetStatus(1: bool status) throws (1: EThriftException.ncTException exp);

    // 40.2 获取网段文档库绑定开关状态
    bool DocLimitm_GetStatus() throws (1: EThriftException.ncTException exp);

    // 40.3 添加网段设置
    void DocLimitm_AddNet(1:ncTNetInfo netInfo) throws (1: EThriftException.ncTException exp);

    // 40.4 编辑网段设置
    void DocLimitm_EditNet(1:ncTNetInfo netInfo) throws (1: EThriftException.ncTException exp);

    // 40.5 删除网段设置
    void DocLimitm_DeleteNet(1:string netId) throws (1: EThriftException.ncTException exp);

    // 40.6 获取网段设置
    list<ncTNetInfo> DocLimitm_GetNet() throws (1: EThriftException.ncTException exp);

    // 40.7 根据ip搜索网段设置
    list<ncTNetInfo> DocLimitm_SearchNet(1:string ip) throws (1: EThriftException.ncTException exp);

    // 40.8 添加绑定文档库设置
    void DocLimitm_AddDocs(1:string netId, 2:list<string> docId) throws (1: EThriftException.ncTException exp);

    // 40.9 删除绑定文档库设置
    void DocLimitm_DeleteDocs(1:string netId, 2:string docId) throws (1: EThriftException.ncTException exp);

    // 40.10 在指定网段设置中获取所有绑定的文档库信息
    list<ncTDocInfo> DocLimitm_GetDocs(1:string netId) throws (1: EThriftException.ncTException exp);

    // 40.11 在指定网段设置中搜索某个绑定的文档库信息
    list<ncTDocInfo> DocLimitm_SearchDocs(1:string netId, 2:string name) throws (1: EThriftException.ncTException exp);

    // 40.12 根据文档库id获取其网段绑定信息
    list<ncTNetInfo> DocLimitm_GetNetByDocId(1:string docId) throws (1: EThriftException.ncTException exp);

    // ----------------------------------------------------------------------------
    // 四十一、文档下载限制管理
    // ----------------------------------------------------------------------------
    // 41.1 增加一条限制信息
    string Usrm_AddDocDownloadLimitInfo(1:ncTDocDownloadLimitInfo info) throws (1: EThriftException.ncTException exp);

    // 41.2 编辑一条限制信息中的限制对象
    void Usrm_EditDocDownloadLimitObject(1:string id, 2:list<ncTDocDownloadLimitObject> userInfos, 3:list<ncTDocDownloadLimitObject> depInfos) throws (1: EThriftException.ncTException exp);

    // 41.3 编辑一条限制信息中的文档上限配置
    void Usrm_EditDocDownloadLimitValue(1:string id, 2:i64 limitValue) throws (1: EThriftException.ncTException exp);

    // 41.4 删除一条限制信息
    void Usrm_DeleteDocDownloadLimitInfo(1:string id) throws (1: EThriftException.ncTException exp);

    // 41.5 获取文档下载限制信息总数
    i64 Usrm_GetDocDownloadLimitInfoCnt() throws (1: EThriftException.ncTException exp);

    // 41.6 分页获取文档下载限制信息
    list<ncTDocDownloadLimitInfo> Usrm_GetDocDownloadLimitInfoByPage(1: i32 start, 2: i32 limit) throws (1: EThriftException.ncTException exp);

    // 41.7 搜索文档下载限制信息
    list<ncTDocDownloadLimitInfo> Usrm_SearchDocDownloadLimitInfoByPage(1:string searchKey, 2: i32 start, 3: i32 limit) throws (1: EThriftException.ncTException exp);

    // 41.8 搜索文档下载限制信息总数
    i64 Usrm_SearchDocDownloadLimitInfoCnt(1:string searchKey) throws (1: EThriftException.ncTException exp);

    // 41.9 获取用户的下载量限制值
    i64 Usrm_GetUserDocDownloadLimitValue(1:string userId) throws (1: EThriftException.ncTException exp);

    // 41.10 设置下载量限制配置的邮件通知状态
    void Usrm_SetDDLEmailNotifyStatus(1: bool status) throws (1: EThriftException.ncTException exp);

    // 41.11 获取下载量限制配置的邮件通知状态
    bool Usrm_GetDDLEmailNotifyStatus() throws (1: EThriftException.ncTException exp);

    // ----------------------------------------------------------------------------
    // 四十二、共享文档配置管理
    // ----------------------------------------------------------------------------
    // 42.1 获取共享文档配置
    bool GetShareDocStatus(1: ncTDocType docType, 2: ncTTemplateType linkType) throws(1: EThriftException.ncTException exp);

    // 42.2 设置共享文档开关状态
    void SetShareDocStatus(1: ncTDocType docType, 2: ncTTemplateType linkType, 3: bool status) throws(1: EThriftException.ncTException exp);

    // ----------------------------------------------------------------------------
    // 四十三、文件留底配置管理
    // ----------------------------------------------------------------------------
    // 43.1 获取文件留底开关状态
    bool GetRetainFileStatus() throws (1: EThriftException.ncTException exp);

    // ----------------------------------------------------------------------------
    // 四十四、权限共享屏蔽组织架构信息管理
    // ----------------------------------------------------------------------------
    // 44.1 设置屏蔽用户信息状态
    void SetHideUserInfoStatus(1: bool status) throws (1: EThriftException.ncTException exp);

    // 44.2 获取屏蔽用户信息状态
    bool GetHideUserInfoStatus() throws (1: EThriftException.ncTException exp);

    // 44.3 设置屏蔽组织架构显示状态
    void HideOum_SetStatus(1: bool status) throws (1: EThriftException.ncTException exp);

    // 44.4 获取屏蔽组织架构显示状态
    bool HideOum_GetStatus() throws (1: EThriftException.ncTException exp);

    // 44.5 添加需要屏蔽组织架构的部门
    void HideOum_Add(1:list<string> departmentIds) throws (1: EThriftException.ncTException exp);

    // 44.6 获取屏蔽组织架构的部门信息
    list<ncTUsrmDepartmentInfo> HideOum_Get() throws (1: EThriftException.ncTException exp);

    // 44.7 根据部门名搜索屏蔽组织架构的部门信息
    list<ncTUsrmDepartmentInfo> HideOum_Search(1:string searchKey) throws (1: EThriftException.ncTException exp);

    // 44.8 根据id删除屏蔽组织架构中的部门
    void HideOum_Delete(1:string departmentId) throws (1: EThriftException.ncTException exp);

    // 44.9 检查用户是否需要屏蔽组织架构
    bool HideOum_Check(1:string userId) throws (1: EThriftException.ncTException exp);

    // 44.10 设置用户共享时搜索配置
    void SetSearchUserConfig (1: ncTSearchUserConfig config) throws (1: EThriftException.ncTException exp);

    // 44.11 获取用户共享时搜索配置
    ncTSearchUserConfig GetSearchUserConfig () throws (1: EThriftException.ncTException exp);

    // ----------------------------------------------------------------------------
    // 四十六、文件改密需要审核配置接口
    // ----------------------------------------------------------------------------
    // 46.1 设置文件改密需要审核状态
    void SetCsfLevelAuditStatus(1: bool status) throws (1: EThriftException.ncTException exp);

    // 46.2 获取文件改密需要审核状态
    bool GetCsfLevelAuditStatus() throws (1: EThriftException.ncTException exp);

    // ----------------------------------------------------------------------------
    // 四十七、外链留底配置管理
    // ----------------------------------------------------------------------------
    // 47.1 设置外链留底开关状态
    void SetRetainOutLinkStatus(1: bool status) throws (1: EThriftException.ncTException exp);

    // 47.2 获取外链留底开关状态
    bool GetRetainOutLinkStatus() throws (1: EThriftException.ncTException exp);

    // ----------------------------------------------------------------------------
    // 四十八、设备绑定查询
    // ----------------------------------------------------------------------------
    // 48.1 获取用户绑定状态信息
    list<ncTDeviceBindUserInfo> Devicem_SearchUsersBindStatus(1: ncTBindStatusSearchScope scope, 2: string searchKey,
                                                    3: i32 start, 4: i32 limit)
                                                    throws(1: EThriftException.ncTException exp)

    // 48.2 获取用户绑定状态数量
    i64 Devicem_SearchUsersBindStatusCnt(1: ncTBindStatusSearchScope scope, 2: string searchKey) throws(1: EThriftException.ncTException exp)

    // ----------------------------------------------------------------------------
    // 四十九、防病毒管理
    // ----------------------------------------------------------------------------
    // 49.1 获取所有防病毒管理员ID
    list<string> GetAllAntivirusAdmin() throws(1: EThriftException.ncTException exp)

    // 49.2 通过登录名添加防病毒管理员
    void AddAntivirusAdmin(1: string loginName) throws(1: EThriftException.ncTException exp)

    // ----------------------------------------------------------------------------
    // 五十、导出日志文件管理
    // ----------------------------------------------------------------------------
    // 50.1 设置日志导出加密开关状态
    void SetExportWithPassWordStatus(1: bool status) throws (1: EThriftException.ncTException exp);

    // 50.2 获取日志导出加密开关状态
    bool GetExportWithPassWordStatus() throws (1: EThriftException.ncTException exp);

    // 50.3 添加导出活跃日志文件任务
    /*
     * @param name: 压缩包名称(log.zip)
     * @param pwd: 压缩包密码
     * @param logCount: EACPLog.GetLogCount 返回值中的 logCount
     * @param param: 生成活跃日志所需的参数
     * @return: 任务 id
     * @throw: 转抛内部调用异常
     */
    string ExportActiveLog (1: string name, 2: string pwd, 3: i64 logCount, 4: EACPLog.ncTExportLogParam param) throws (1: EThriftException.ncTException exp);

    // 50.4 添加导出历史日志文件任务
    /**
     * @param logId: 历史日志文件 id
     * @param validSeconds: 下载请求的有效时长
     * @param pwd: 压缩包密码
     * @return: 任务 id
     * @throw: 转抛内部调用异常
     */
    string ExportHistoryLog (1: string logId, 2: i64 validSeconds, 3: string pwd) throws (1: EThriftException.ncTException exp);

    // 50.5 获取日志文件信息
    string GetCompressFileInfo (1: string taskId) throws (1: EThriftException.ncTException exp)

    // 50.6 获取日志文件生成状态
    bool GetGenCompressFileStatus (1: string taskId) throws (1: EThriftException.ncTException exp)

    // ----------------------------------------------------------------------------
    // 五十一、回收站配置管理
    // ----------------------------------------------------------------------------
    // 51.1 设置回收站配置
    void SetRecycleInfo (1: ncTRecycleInfo info, 2: string cid) throws (1: EThriftException.ncTException exp);

    // 51.2 获取回收站配置
    ncTRecycleInfo GetRecycleInfo (1: string cid) throws (1: EThriftException.ncTException exp);

    // 51.3 删除回收站配置
    void DelRecycleInfo (1: string cid) throws (1: EThriftException.ncTException exp);

    // 51.4 获取所有回收站配置
    list<ncTRecycleInfo> GetRecycleInfos () throws (1: EThriftException.ncTException exp);

    // ----------------------------------------------------------------------------
    // 五十二、短信服务器配置管理
    // ----------------------------------------------------------------------------
    // 52.1 获取短信服务器配置
    string SMS_GetConfig() throws (1: EThriftException.ncTException exp);

    // 52.2 设置短信服务器配置
    void SMS_SetConfig(1: string config) throws (1: EThriftException.ncTException exp);

    // 52.3 测试短信服务器
    void SMS_Test(1: string config) throws (1: EThriftException.ncTException exp);

    // 52.4 发送短信验证码
    void SMS_SendVcode(1: string account, 2: string password, 3: string telNumber) throws (1: EThriftException.ncTException exp);

    // 52.5 激活账号
    string SMS_Activate(1: string account, 2: string password, 3: string telNumber, 4: string mailAddress, 5: string verifyCode) throws (1: EThriftException.ncTException exp);

    // 五十四、活跃用户统计管理
    // ----------------------------------------------------------------------------
    // 54.1 获取月度活跃报表信息
    ncTActiveReportInfo GetActiveReportMonth(1: string inquireDate) throws (1: EThriftException.ncTException exp);

    // 54.2 获取年度活跃报表数信息
    ncTActiveReportInfo GetActiveReportYear(1: string inquireDate) throws (1: EThriftException.ncTException exp);

    // 54.3 创建导出月度活跃报表任务
    string ExportActiveReportMonth(1: string name, 2: string inquireDate) throws (1: EThriftException.ncTException exp);

    // 54.4 创建导出年度活跃报表任务
    string ExportActiveReportYear(1: string name, 2: string inquireDate) throws (1: EThriftException.ncTException exp);

    // 54.5 获取生成活跃报表状态
    bool GetGenActiveReportStatus(1: string taskId) throws (1: EThriftException.ncTException exp);

    // 54.6 获取活跃报表文件信息
    string GetActiveReportFileInfo(1: string taskId) throws (1: EThriftException.ncTException exp);

    // 54.7 设置活跃报表邮件通知开关状态
    void SetActiveReportNotifyStatus(1: bool status) throws (1: EThriftException.ncTException exp);

    // 54.8 获取活跃报表邮件通知开关状态
    bool GetActiveReportNotifyStatus() throws (1: EThriftException.ncTException exp);

    // 54.9 设置通知到爱数的邮件接收地址
    void SetEisooRecipientEmail(1: list<string> emailList) throws (1: EThriftException.ncTException exp);

    // 54.10 获取通知到爱数的邮件接收地址
    list<string> GetEisooRecipientEmail() throws (1: EThriftException.ncTException exp);

    // ----------------------------------------------------------------------------
    // 五十五、用户角色管理
    // ----------------------------------------------------------------------------
    // 55.1 添加角色
    string UsrRolem_Add(1: ncTRoleInfo roleInfo) throws (1: EThriftException.ncTException exp);

    // 55.2 获取角色
    list<ncTRoleInfo> UsrRolem_Get(1: string userId) throws (1: EThriftException.ncTException exp);

    // 55.3 编辑角色
    void UsrRolem_Edit(1: string userId, 2: ncTRoleInfo roleInfo) throws (1: EThriftException.ncTException exp);

    // 55.4 删除角色
    void UsrRolem_Delete(1: string userId, 2: string roleId) throws (1: EThriftException.ncTException exp);

    // 55.5 设置成员包含添加和编辑成员
    void UsrRolem_SetMember(1: string userId, 2: string roleId, 3:ncTRoleMemberInfo memberInfo) throws (1: EThriftException.ncTException exp);

    // 55.6 获取成员列表
    list<ncTRoleMemberInfo> UsrRolem_GetMember(1: string userId, 2: string roleId) throws (1: EThriftException.ncTException exp);

    // 55.7 在角色成员列表中根据用户名搜索用户
    list<ncTRoleMemberInfo> UsrRolem_SearchMember(1: string userId, 2: string roleId, 3: string name) throws (1: EThriftException.ncTException exp);

    // 55.8 删除成员
    void UsrRolem_DeleteMember(1: string userId, 2: string roleId, 3: string memberId) throws (1: EThriftException.ncTException exp);

    // 55.9 获取用户角色信息
    list<ncTRoleInfo> UsrRolem_GetRole(1: string userId) throws(1: EThriftException.ncTException exp)

    // 55.10 在所选角色中根据成员id获取详细信息
    ncTRoleMemberInfo UsrRolem_GetMemberDetail(1: string userId, 2: string roleId, 3: string memberId) throws (1: EThriftException.ncTException exp);

    // 55.11 根据用户角色获取用户所能看到的根组织
    list<ncTRootOrgInfo> UsrRolem_GetSupervisoryRootOrg(1: string userId, 2: string roleId) throws(1: EThriftException.ncTException exp)

    // 55.12 根据角色搜索部门
    list<ncTUsrmDepartmentInfo> UsrRolem_SearchDepartments(1: string userId, 2: string roleId, 3: string searchKey, 4: i32 start, 5: i32 limit)
                                                           throws (1: EThriftException.ncTException exp)

    // 55.13 在用户角色所管理的部门中搜索用户
    list<ncTSearchUserInfo> UsrRolem_SearchSupervisoryUsers(1: string userId, 2: string roleId, 3: string key, 4: i32 start, 5: i32 limit)
                                                             throws(1: EThriftException.ncTException exp)

    // 55.15 获取指定角色下所有邮箱列表
    list<string> UsrRolem_GetMailListByRoleId(1:string roleId) throws(1: EThriftException.ncTException exp)

    // 55.16 检查成员是否存在
    bool UsrRolem_CheckMemberExist(1: string roleId, 2: string memberId) throws (1: EThriftException.ncTException exp);

    // 五十六、文件抓取配置管理
    // ----------------------------------------------------------------------------
    // 56.1 设置文档抓取总开关
    void SetFileCrawlStatus(1: bool status) throws (1: EThriftException.ncTException exp);

    // 56.2 获取文档抓取总开关
    bool GetFileCrawlStatus() throws (1: EThriftException.ncTException exp);

    // 56.3 新建文档抓取配置
    i32 AddFileCrawlConfig(1: ncTFileCrawlConfig fileCrawlConfig) throws (1: EThriftException.ncTException exp);

    // 56.4 设置文档抓取配置
    void SetFileCrawlConfig(1: ncTFileCrawlConfig fileCrawlConfig) throws (1: EThriftException.ncTException exp);

    // 56.5 删除文档抓取配置
    void DeleteFileCrawlConfig(1: i32 strategyId) throws (1: EThriftException.ncTException exp);

    // 56.6 获取文档抓取配置数
    i64 GetFileCrawlConfigCount() throws (1: EThriftException.ncTException exp);

    // 56.7 分页获取文档抓取配置
    list<ncTFileCrawlConfig> GetFileCrawlConfig(1: i32 start, 2: i32 limit) throws (1: EThriftException.ncTException exp);

    // 56.8 根据关键字分页搜索文档抓取配置数
    i64 GetSearchFileCrawlConfigCount (1: string searchKey) throws (1: EThriftException.ncTException exp);

    // 56.9 根据关键字分页搜索文档抓取配置
    list<ncTFileCrawlConfig> SearchFileCrawlConfig(1: string searchKey,
                                                   2: i32 start,
                                                   3: i32 limit)
                                                   throws (1: EThriftException.ncTException exp);

    // 56.10 根据用户ID获取文件抓取配置(不存在时返回结果的strategyId为-1)
    ncTFileCrawlConfig GetFileCrawlConfigByUserId(1: string userId) throws (1: EThriftException.ncTException exp);

    // 56.11 设置控制台是否显示抓取策略开关
    void SetFileCrawlShowStatus(1: bool status) throws (1: EThriftException.ncTException exp);

    // 56.12 获取控制台是否显示抓取策略开关
    bool GetFileCrawlShowStatus() throws (1: EThriftException.ncTException exp);

    // ----------------------------------------------------------------------------
    // 五十七、个人文档自动归档策略管理
    // ----------------------------------------------------------------------------
    // 57.1. 开启/禁用自动归档策略
    // void SetDocAutoArchiveStatus(1: bool status) throws (1: EThriftException.ncTException exp);

    // 57.2. 获取自动归档策略启用/禁用状态
    // bool GetDocAutoArchiveStatus() throws (1: EThriftException.ncTException exp);

    // 57.3. 增加一条自动归档策略配置
    // ncTAutoArchiveConfig AddAutoArchiveConfig(1:ncTAutoArchiveConfig config) throws (1: EThriftException.ncTException exp);

    // 57.4. 编辑一条自动归档策略配置
    // ncTAutoArchiveConfig EditAutoArchiveConfig(1:ncTAutoArchiveConfig config) throws (1: EThriftException.ncTException exp);

    // 57.5. 删除一条自动归档策略配置
    // void DeleteAutoArchiveConfig(1:string configId) throws (1: EThriftException.ncTException exp);

    // 57.6. 获取自动归档策略配置总数
    // i64 GetAutoArchiveConfigCount(1:string searchKey) throws (1: EThriftException.ncTException exp);

    // 57.7. 分页搜索自动归档策略配置
    /* list<ncTAutoArchiveConfig> SearchAutoArchiveConfigByPage(1: i32 start,
                                                             2: i32 limit,
                                                             3: string searchKey)
                                                             throws (1: EThriftException.ncTException exp); */

    // 57.8. 获取所有待归档用户id
    // list<string> GetAllAutoArchiveUserId() throws (1: EThriftException.ncTException exp);

    // 57.9. 根据用户Id获取最后生效的策略
    // ncTAutoArchiveConfig GetAutoArchiveConfigByUserId(1: string userId) throws (1: EThriftException.ncTException exp);

    // ----------------------------------------------------------------------------
    // 五十八、个人文档自动清理策略管理
    // ----------------------------------------------------------------------------
    // 58.1. 开启/禁用自动清理策略
    void SetDocAutoCleanStatus(1: bool status) throws(1: EThriftException.ncTException exp);

    // 58.2. 获取自动清理策略启用/禁用状态
    bool GetDocAutoCleanStatus() throws(1: EThriftException.ncTException exp);

    // 58.3. 设置管理员级别的回收站中数据保留时间
    void SetGlobalRecycleRetentionConfig(1: ncTGlobalRecycleRetentionConfig config) throws(1: EThriftException.ncTException exp)

    // 58.4. 获取管理员级别的回收站中数据保留时间
    ncTGlobalRecycleRetentionConfig GetGlobalRecycleRetentionConfig() throws(1: EThriftException.ncTException exp)

    // 58.5. 增加一条自动清理策略配置
    ncTAutoCleanConfig AddAutoCleanConfig(1: ncTAutoCleanConfig config) throws(1: EThriftException.ncTException exp)

    // 58.6. 编辑一条自动清理策略配置
    ncTAutoCleanConfig EditAutoCleanConfig(1: ncTAutoCleanConfig config) throws(1: EThriftException.ncTException exp)

    // 58.7. 删除一条自动归档策略配置
    void DeleteAutoCleanConfig(1: string configId) throws(1: EThriftException.ncTException exp)

    // 58.8. 分页搜索自动清理策略配置
    list<ncTAutoCleanConfig> SearchAutoCleanConfigByPage(1: i32 start,
                                                         2: i32 limit,
                                                         3: string searchKey)
                                                         throws (1: EThriftException.ncTException exp);

    // 58.9. 获取自动清理策略配置总数
    i64 GetAutoCleanConfigCount(1:string searchKey) throws (1: EThriftException.ncTException exp);

    // 58.10. 获取所有待清理用户id
    list<string> GetAllAutoCleanUserId() throws (1: EThriftException.ncTException exp);

    // 58.11. 根据用户id获取最后生效的策略
    ncTAutoCleanConfig GetAutoCleanConfigByUserId(1: string userId) throws (1: EThriftException.ncTException exp);

    // 五十九、指定文档库病毒扫描管理
    // ----------------------------------------------------------------------------
    // 59.1 开始指定文档库病毒扫描任务
    list<string> StartScanVirusTask(1: list<string> userIds,
                                    2: list<string> departIds,
                                    3: list<string> cids)
                                    throws (1: EThriftException.ncTException exp);

    // 59.2 暂停扫描任务
    void StopScanVirusTask() throws (1: EThriftException.ncTException exp);

    // 59.3 继续扫描任务
    void ContinueScanVirusTask() throws (1: EThriftException.ncTException exp);

    // 59.4 取消扫描任务
    void CancelScanVirusTask() throws (1: EThriftException.ncTException exp);

    // 59.5 获取本次扫描染毒文件数
    i64 GetVirusInfoCnt() throws (1: EThriftException.ncTException exp);

    // 59.6 分页获取本次扫描染毒文件信息
    list<ncTVirusInfo> GetVirusInfoByPage(1: i32 start, 2: i32 limit) throws (1: EThriftException.ncTException exp);

    // 59.7 获取扫描结果
    ncTScanTaskInfo GetScanVirusTaskResult() throws (1: EThriftException.ncTException exp);

    // 59.8 向所有节点上传病毒库
    void SetGlobalVirusDB(1: ncTVirusDBInfo virusDB) throws (1: EThriftException.ncTException exp);

    // 59.9 向当前节点上传病毒库
    void SetLocalVirusDB(1: ncTVirusDBInfo virusDB) throws (1: EThriftException.ncTException exp);

    // 59.10 获取病毒库信息
    ncTVirusDBInfo GetVirusDB() throws (1: EThriftException.ncTException exp);

    // 59.11 杀毒选件是否授权过，存在已激活或已过期的选件都会返回True
    bool GetAntivirusOptionAuthStatus() throws (1: EThriftException.ncTException exp);

    // 59.12 杀毒完成发送邮件通知超级管理员或者安全管理员
    void NotifyScanFinish() throws (1: EThriftException.ncTException exp);

    // 59.13 测试病毒库ftp服务器是否可用
    bool VirusFTPServerTest() throws (1: EThriftException.ncTException exp);

    // 59.14 设置杀毒白名单
    void SetAntivirusWhiteList (1: list<string> cids) throws (1: EThriftException.ncTException exp);

    // 59.15 获取杀毒白名单
    list<string> GetAntivirusWhiteList () throws (1: EThriftException.ncTException exp);

    // 59.16 删除移除主分站点关系后，分站点依旧保存在主站点的杀毒任务
    void DeleteInvalidSlaveSiteVirusTask(1:string siteID) throws (1: EThriftException.ncTException exp);

    // 59.17 获取下载病毒库url
    string GetVirusDBDownloadUrl() throws (1: EThriftException.ncTException exp);

    // 59.17 设置下载病毒库url
    void SetVirusDBDownloadUrl(1:string virusDBDownloadUrl) throws (1: EThriftException.ncTException exp);

    // 六十、本地同步策略
    // ----------------------------------------------------------------------------
    // 60.1 增加一条本地同步策略配置
    string AddLocalSyncConfig(1:ncTLocalSyncConfig config) throws (1: EThriftException.ncTException exp);

    // 60.2 编辑一条本地同步策略配置
    void EditLocalSyncConfig(1:ncTLocalSyncConfig config) throws (1: EThriftException.ncTException exp);

    // 60.3 删除一条本地同步策略配置
    void DeleteLocalSyncConfig(1:string strategyId) throws (1: EThriftException.ncTException exp);

    // 60.4 获取本地同步策略配置总数
    i64 GetLocalSyncConfigCount(1:string searchKey) throws (1: EThriftException.ncTException exp);

    // 60.5 分页搜索本地同步策略配置
    list<ncTLocalSyncConfig> SearchLocalSyncConfigByPage(1: i32 start,
                                                         2: i32 limit,
                                                         3: string searchKey)
                                                         throws (1: EThriftException.ncTException exp);

    // 60.6 根据用户Id获取最后生效的策略
    ncTLocalSyncConfig GetLocalSyncConfigByUserId(1: string userId) throws (1: EThriftException.ncTException exp);

    // 六十一、用户空间使用信息导出管理
    // ----------------------------------------------------------------------------
    /**
     * 61.1 创建导出报表任务
     * @param name : 报表文件的名字，拓展名为".csv"
     * @param objType : 统计的文档库类型，可取值：1/3/5
     * @return : 服务端生成的任务id
     */
    string ExportSpaceReport(1: string name, 2: i32 objType) throws (1: EThriftException.ncTException exp);

    // 61.2 获取导出报表任务状态
    bool GetGenSpaceReportStatus(1: string taskId) throws (1: EThriftException.ncTException exp);

    // 61.3 获取报表文件的路径
    string GetSpaceReportFilePath(1: string taskId) throws (1: EThriftException.ncTException exp);

    // 六十二、webhook 管理
    // ----------------------------------------------------------------------------
    // 62.1 获取 webhook 配置信息
    ncTWebhookConfig GetWebhookConfig () throws (1: EThriftException.ncTException exp);

    // 62.2 设置 webhook 配置信息
    void SetWebhookConfig (1: ncTWebhookConfig config) throws (1: EThriftException.ncTException exp);

    // 62.3 测试 webhook 通知 URL 是否可用
    bool TestWebhookConfig(1:string url) throws (1: EThriftException.ncTException exp);

    // 六十三、快速入门管理
    // 63.1 获取用户是否显示“快速入门”（现阶段只支持控制台）
    bool NeedQuickStart(1:string userId 2:i32 osType) throws (1: EThriftException.ncTException exp);

    // 63.2 更新用户是否显示"快速入门"状态（现阶段只支持控制台）
    void SetQuickStartStatus(1:string userId 2:bool status 3:i32 osType) throws (1: EThriftException.ncTException exp);
}
