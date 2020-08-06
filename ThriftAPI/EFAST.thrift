/*******************************************************************************************
EFAST.thrift
    Copyright (c) Eisoo Software, Inc.(2012 - 2013), All rights reserved

Purpose:
    EFAST manager service.

Author:
    liu.wenxuan (liu.wenxuan@eisoo.com)

Creating Time:
    2012-05-29
*******************************************************************************************/

include "EThriftException.thrift"

/**
 * Thrift端口号
 */
const i32 NCT_EFAST_PORT = 9121

enum ncTServiceState {
    NCT_SERVICE_RUN_STATE  = 0,         /* 运行状态 */
    NCT_SERVICE_STOP_STATE    = 1,      /* 停止状态 */
}

// 部门权限
struct ncTDepartPerm {
    1: i32             permValue;          // 权限值（1-127）
    2: i64             endTime;            // 截止时间，单位为微秒
}

// 新建文档库参数
struct ncTAddCustomDocParam {
    1: string                       name;            // 名称
    2: string                       typeName;        // 类型名
    3: string                       createrId;       // 创建人id
    4: list<string>                 ownerIds;        // 所有者id
    5: i64                          spaceQuota;      // 配额
    6: string                       ossId;           // 对象存储id
    7: optional string              relateDepartId;  // 关联部门id
    8: optional ncTDepartPerm       perm;            // 部门权限
}

struct ncTCustPerm {
    1: string           accessorId;         // 访问者id
    2: i16              accessorType;       // 访问者类型
    3: bool             isAllowed;          // 允许/拒绝
    4: i32              permValue;          // 权限值
    5: i64              endTime;            // 截止时间
}

// 东华大学自动同步文档库参数
struct ncTAddCustomDocParamEx {
    1: string           name;               // 名称
    2: string           typeName;           // 类型名
    3: string           createrId;          // 创建人id
    4: list<string>     ownerIds;           // 所有者id
    5: i64              spaceQuota;         // 配额
    6: string           objId;              // 自定义的对象id，不能和已有的冲突
    7: list<ncTCustPerm>  permConfigs;      // 权限配置
    8: string           ossId;              // 对象存储id
}

// 编辑文档库参数
struct ncTEditCustomDocParam {
    1: string            docId;            // 文档id
    2: string            name;             // 名称
    3: string            typeName;         // 类型名
    4: list<string>      ownerIds;         // 所有者id
    5: i64               spaceQuota;       // 配额
    6: string            userId;           // 操作者id
    7: string            ossId;            // 对象存储id
}

// 删除文档库参数
struct ncTDeleteCustomDocParam {
    1: string            docId;             // 文档id
    2: string            userId;            // 操作者id
}

// 用户信息
struct ncTUserInfo {
    1: string            id;                // 用户id
    2: string            name;              // 用户显示名
    3: string            account;           // 用户账号
}

//对象存储信息
struct ncTDocOSSInfo {
    1: string ossId;                         // 对象存储ID
    2: string ossName;                       // 对象存储名称
    3: string siteName;                      // 对象存储归属站点
    4: bool enabled;                         // 对象存储状态
    5: i32 type,                             // 0 表示当前站点配置、管理的对象存储，1 表示分站点同步到总站点的对象存储
}

// 文档库信息
struct ncTCustomDocInfo {
    1: string            docId;            // 文档id
    2: string            name;             // 名称
    3: string            typeName;         // 类型名
    4: string            createrId;        // 创建人id
    5: string            createrName;      // 创建人名称
    6: list<ncTUserInfo> ownerInfos;       // 所有者信息
    7: i64               spaceQuota;       // 配额
    8: i64               usedSize;         // 已用空间
    9: double            usedSpaceRate;    // 空间使用率
    10:ncTDocOSSInfo     ossInfo;          // 对象存储信息
    11:string            relateDepartName; // 关联部门名
    12:string            relateDepartId;   // 关联部门id
    13:i32               displayOrder;     // 文档库显示顺序
}

// 排序(搜索)字段
enum ncTSortKey {
    NCT_NAME = 1,                     // 文档库名称
    NCT_LIBTYPE = 2,                  // 文档库类型
    NCT_CREATER = 3,                  // 文档库创建者
    NCT_OWNER = 4,                    // 文档库所有者
    NCT_USEDSPACERATE = 5,            // 空间使用率
    NCT_ORDER = 6,                    // 显示顺序
    NCT_NO = 0,                       // 不进行排序
}

// 排序类型
enum ncTSortType {
    NCT_SORT_DESC = 0,                // 降序排列
    NCT_SORT_ASC = 1,                 // 升序排列
}

// 分页获取文档库参数
struct ncTGetPageDocParam {
    1: required string userId;                  // 用户id (必须)
    2: optional ncTSortKey sortKey;             // 排序关键字
    3: optional ncTSortType sortType;           // 排序类型
    4: optional list<string> docNames;          // 文档库名字，支持选择多个，模糊匹配
    5: optional list<string> docTypes;          // 文档库类型，支持选择多个，模糊匹配
    6: optional list<string> docOwners;         // 文档库所属者，支持选择多个，模糊匹配
    7: optional list<string> docCreaters;       // 文档库创建者，支持选择多个，模糊匹配
    8: optional string relateDepartName;        // 关联部门名
    9: required i32 start;                      // 开始文档库号 (必须)
    10: required i32 limit;                     // 条数 (必须)
}

// 批量新建文档库参数
struct ncTBatchAddCustomDocParam {
    1: list<string>             relateDepartIds;    // 部门id
    2: bool                     includeCurDepart;   // 是否包含当前部门
    3: optional i32             level;              // 部门层级（-1：所有层级子部门，-2：最下级部门，> 0 : 自定义层级）
    4: string                   typeName;           // 类型名
    5: string                   ownerId;            // 所有者（"-1"为部门组织管理员，否则为指定用户）
    6: optional ncTDepartPerm   perm;               // 部门权限
    7: i64                      spaceQuota;         // 配额
    8: string                   createrId;          // 创建者id
}

// 创建文档库失败信息
struct ncTAddCustomDocFailInfo {
    1: string       docName;                // 文档库名
    2: string       detailInfo;             // 详细信息
}

// 批量创建文档库的执行结果
struct ncTBatchAddCustomDocResult {
    1: i32                              totalDepartNum;         // 创建总数
    2: i32                              successNum;             // 成功数
    3: i32                              failNum;                // 失败数
    4: list<ncTAddCustomDocFailInfo>    failInfos;              // 失败信息
}

// 新建归档库参数
struct ncTAddArchiveDocParam {
    1: string            name;            // 名称
    2: string            createrId;       // 创建人id
    3: string            ownerId;         // 所有者id
    4: i64               spaceQuota;      // 配额
    5: string            ossId;           // 对象存储id
}

// 编辑归档库参数
struct ncTEditArchiveDocParam {
    1: string            docId;            // 文档id
    2: string            name;             // 名称
    3: string            ownerId;          // 所有者id
    4: i64               spaceQuota;       // 配额
    5: string            userId;           // 操作者id
    6: string            ossId;            // 对象存储id
}

// 删除归档库参数
struct ncTDeleteArchiveDocParam {
    1: string            docId;             // 文档id
    2: string            userId;            // 操作者id
}

// 归档库信息
struct ncTArchiveDocInfo {
    1: string            docId;            // 文档id
    2: string            name;             // 名称
    3: string            createrId;        // 创建人id
    4: string            createrName;      // 创建人名称
    5: ncTUserInfo       ownerInfo;        // 所有者信息
    6: i64               spaceQuota;       // 配额
    7: i64               usedSize;         // 已用空间
    8: double            usedSpaceRate;    // 空间使用率
    9: ncTDocOSSInfo     ossInfo;          // 对象存储信息
}

// 用户配额信息
struct ncTSpaceQuotaInfo {
    1: i64            spaceQuota;      // 用户总空间
    2: i64            usedSize;        // 用户已用空间
}

// 系统回收站入口文档相关信息
struct ncTSysRecycleEntryDocInfo {
    1: string docId;                                // 文件GNS路径
    2: string docType;                              // 入口文档类型 "userdoc":用户文档, "customdoc":自定义组织文档
    3: string typeName;                             // 文档类型的显示名称
    4: string docName;                              // 文档的显示名称
    5: bool isDeleted;                              // 文档库是否被删除
    6: string deleterName;                          // 文档库删除者名称
    7: i64 deleteTime;                              // 文档库删除时间
    8: i64 serverTime;                              // 服务器时间
}

// 错误码
const string NCT_EFAST_ERR_PROVIDER_NAME = "EFASTThrift"
enum ncTEFASTError {
    NCT_FAILED_TO_GET_EFAST_DISPATCHER = 10001,            // 获取 ncIEFASTDispatcher 对象失败
    NCT_FAILED_TO_GET_NET_SERVER = 10002,                  // 获取 ncNetServer 对象失败
    NCT_EFAST_PTHREAD_CREATE_ERROR = 10003,                // 创建线程失败
    NCT_EFASTSERVER_HAS_INIT_ERROR = 10004,                // 已经启动EFASTSERVER服务
    NCT_EFASTSERVER_NOT_INIT_ERROR = 10005,                // 已经卸载EFASTServer服务
    NCT_FAILED_TO_GET_EFTSEARCH_SERVER = 10006,            // 获取 ncIEFTSearchHttpMgr 对象失败
    NCT_SAME_HTTP_AND_HTTPS_PORT_ERROR = 10007,            // Https 和 Http 的端口[%d]不能设置成一样

    FAILED_TO_CREATE_DB_EDOC_MANANGER = 20001,             // 创建dbEDocManager实例失败
    FAILED_TO_CREATE_ENTRY_DOC_MANAGER = 20002,            // 创建entryDocManager实例失败
    FAILED_TO_CREATE_ENTRY_DOC_IOC = 20003,                // 创建entryDocIOC实例失败
    SPACE_EXCEEDS_THE_MAX_LIMIT = 20004,                   // 用户空间不足
    NCT_INVALID_QUOTA = 20005,                             // 配额空间非法
    SET_QUOTA_ERROR = 20006,                               // 设置配额错误
    UPDATE_MANAGER_SPACE_ERROR =20007,                     // 更新用户空间错误
    NCT_SITE_NOT_EXIST = 20008,                            // 站点不存在
    NCT_SITE_HAS_BEEN_MOVED = 20009,                       // 站点被移除
    NCT_MUTITENANT_CREATER_BELONG_ONE_OU = 20010,          // 多租户模式下非admin创建者只能属于一个组织
    CANT_SET_ADMIN_TO_OWNER = 20011,                       // 所有者不能设为admin
    NCT_MUTITENANT_OWNER_BELONG_ONE_OU = 20012,            // 多租户模式下所有者只能属于一个组织
    NCT_MUTITENANT_OWNER_CREATER_BELONG_ONE_OU = 20013,    // 多租户模式下文档库创建者和所有者必须属于同一个组织
    NCT_DEPARTMENT_NOT_EXIST = 20014,                      // 部门不存在
    NCT_DEPART_HAS_RELATE_CUSTOM_DOC = 20015,              // 部门已有关联文档库
    NCT_INVALID_PERM_VALUE = 20016,                        // 权限值非法
    NCT_TIME_AHEAD_SERVER_TIME = 20017,                    // 设置的时间早于服务器时间
    NCT_CONFLICATED_WITH_ARCHIVE_DOC_NAME = 20019,         // 该名称与归档库名称冲突
    NCT_CONFLICATED_WITH_CUSTOM_DOC_NAME = 20020,          // 该名称与自定义文档库名称冲突
    NCT_CONFLICATED_WITH_USER_DOC_NAME = 20021,            // 该名称与个人文库名称冲突
    CREATER_NOT_EXISTS = 20022,                            // 创建者不存在
    NCT_USER_NOT_REAL_NAME_AUTH = 20023,                   // 用户未实名认证
    NON_MANAGER_CANT_CREATE = 20024,                       // 非组织文档管理员不能创建组织文档
    NO_OWNER = 20025,                                      // 不包含所有者
    OWNER_NOT_EXISTS = 20026,                              // 所有者不存在
    OWNER_DISABLE = 20027,                                 // 无效的用户
    NCT_INVALID_DOC_LIB_NAME = 20028,                      // 库名不合法，可能字符过长或包含 \ / : * ? " < > | 特殊字符。
    NCT_INVALID_DOC_LIB_TYPE_NAME = 20029,                 // 库类型名不合法，可能字符过长或包含 \ / : * ? " < > | 特殊字符。
    NCT_OBJ_ID_EXISTS = 20030,                             // 无法新建文档库，文档库的objId已经存在
    EDITER_NOT_EXISTS = 20031,                             // 编辑者不存在
    DOC_ID_NOT_EXISTS = 20032,                             // docId不存在
    NOT_CREATER_CANT_EDIT = 20033,                         // 不是文档的创建者，不能编辑该文档
    GET_QUOTA_ERROR = 20034,                               // 获取配额错误
    NOT_CREATER_CANT_DELETE = 20035,                       // 不是文档的创建者，不能删除该文档
    NCT_INVALID_LIMIT_VALUE = 20036,                       // limit参数错误，不应小于-1。
    NCT_USER_CANNOT_BATCH_ADD_DOC = 20037,                 // 当前用户无法发起批量创建
    NCT_NO_SELECT_DEPARTMENT = 20038,                      // 未选择部门
    NCT_INVALID_DEPARTMENT_LEVEL = 20039,                  // 部门层级非法（小于-2）
    NCT_OTHER_TASK_IS_PROCESSING = 20040,                  // 已有任务在处理中
    NCT_TASK_NOT_EXIST_OR_TIME_OUT = 20041,                // 任务不存在或已超时
    NCT_CUSTOM_DOC_DISPLAY_ORDER_INVALID = 20042,          // 自定义文档库的displayorder不合法
    CHECK_ARCHIVE_DOC_EMPTY_ERROR = 20043,                 // 当前归档库不存在归档数据
    ARCHIVE_DOC_NOT_EMPTY = 20044,                         // 当前归档库中已存有归档数据
    NCT_ARCHIVE_DOC_NOT_SUPPORT_TYPE_SORT = 20045,         // 归档库不支持类型排序
    USER_DOC_NOT_EXISTS = 20046,                           // 用户文档库不存在
    NOT_MOVABLE_DOC_TYPE = 20047,                          // 不是可移动的文档库类型
    QUOTA_NOT_ENOUGH = 20048,                              // 配额不足
    INVALID_DOC_TYPE = 20049,                              // 非法的文档库类别
    USER_NOT_EXISTS = 20050,                               // 用户不存在
    USER_DOC_EXISTS = 20051,                               // 个人文档库已存在
    NCT_ENTRY_DOC_NOT_EXIST = 20052,                       // 入口文档不存在
    DELETER_NOT_EXISTS = 20053,                            // 删除者不存在
    NCT_OSS_NOT_EXIST = 20054,                             // 对象存储不存在
    NCT_OSS_HAS_BEEN_DISABLED = 20055,                     // 对象存储已禁用
    FAILED_TO_CREATE_ETS_OSS_MANAGER = 20056,              // 创建etsOSSManager实例失败
}


/**
 * EFAST thift 管理接口
 */
service ncTEFAST {
    ///////////////////////////////////
    //    以下部分是 EFAST 基础配置接口。
    ///////////////////////////////////
    /**
     * 启动 EFAST 服务, 启动服务后才能获取端口和处理池信息
     *
     * @throw EThriftException.ncTException : 1. 转抛底层转抛的输入参数错误
     *                                        2. 底层其他异常转抛
     */
    void EFAST_Start () throws (1: EThriftException.ncTException exp),

    /**
     * 停止 EFAST 服务, 停止服务后才能设置端口和处理池信息
     *
     * @throw EThriftException.ncTException : 停止时出现异常
     */
    void EFAST_Stop () throws (1: EThriftException.ncTException exp),

    /**
     * 获取 EFAST 服务状态
     *
     * @return ncTSynServiceState : 获取 EFAST 数据服务状态, 当 EFAST 服务是启动状态，返回 NCT_SERVICE_RUN_STATE;
     *                              当 EFAST 服务是停止状态，返回 NCT_SERVICE_STOP_STATE
     */
    ncTServiceState EFAST_GetServiceState (),


    /////////////////////////////////////////
    //    以下部分是 EFAST EFSHttp 模块接口。
    /////////////////////////////////////////

    /**
     * 设置 EFAST EFSHttp 数据端口号
     *
     * @param port : 端口号配置, 默认为 9123，范围[9122, 9140],不能和 EFAST 设置的数据端口号一样
     *
     * @throw EThriftException.ncTException : 1. 底层其他异常转抛
     *                                        2. EFAST 服务为启动状态抛错
     *                                        3. 与 EFAST 数据服务已经设置的端口重复
     */
    void EFSHttp_SetPort (1: i32 port) throws (1: EThriftException.ncTException exp),

    /**
     * 获取 EFAST EFSHttp 数据端口号
     *
     * @return i32: 端口编号
     * @throw EThriftException.ncTException : 1. 转抛底层转抛的输入参数错误
     *                                        2. 底层其他异常转抛
     *                                        3. EFAST 服务为停止状态抛错
     */
    i32 EFSHttp_GetPort () throws (1: EThriftException.ncTException exp),

    /**
     * 设置 EFAST EFSHttp 的处理池数目.
     *
     * @param poolCount : 同步服务处理池数目, 默认为100 ，范围为 [1, 200]
     *
     * @throw EThriftException.ncTException : 1. 转抛底层转抛的输入参数错误
     *                                        2. 底层其他异常转抛
     *                                        3. EFAST 服务为启动状态抛错
     */
    void EFSHttp_SetMaxConcurrency (1: i32 processPoolCount)
                                      throws (1: EThriftException.ncTException exp),

    /**
     * 获取 EFAST EFSHttp 的处理池数目.
     *
     *@return i32 : 启动处理池中处理器个数
     *
     * @throw EThriftException.ncTException : 1. 转抛底层转抛的输入参数错误
     *                                        2. 底层其他异常转抛
     *                                        3. EFAST 服务为停止状态抛错
     */
    i32 EFSHttp_GetMaxConcurrency ()
                                     throws (1: EThriftException.ncTException exp),

    /**
     * 创建个人文档
     *
     * @ret: 无返回
     * @throw EThriftException.ncTException
     */
    void EFAST_AddUserDoc (1: string userId, 2: i64 totalQuotaBytes, 3: string responsiblePersonId, 4: string ossId)
        throws (1: EThriftException.ncTException exp);

    /**
     * 新建自定义文档库
     *
     * @ret: 返回创建成功后的id
     * @throw EThriftException.ncTException
     */
    string EFAST_AddCustomDoc (1: ncTAddCustomDocParam info)
        throws (1: EThriftException.ncTException exp);

    /**
     * 新建自定义文档库，指定objId
     *
     * @ret: 返回创建成功后的id
     * @throw EThriftException.ncTException
     */
    string EFAST_AddCustomDocEx (1: ncTAddCustomDocParamEx info)
        throws (1: EThriftException.ncTException exp);

    /**
     * 编辑自定义文档库
     *
     * @ret: 无返回
     * @throw EThriftException.ncTException
     */
    void EFAST_EditCustomDoc (1: ncTEditCustomDocParam info)
        throws (1: EThriftException.ncTException exp);

    /**
     * 设置自定义文档库的管理员
     *
     * @ret: 无返回
     * @throw EThriftException.ncTException
     */
    void EFAST_EditCustomDocManager (1: string docId, 2: string userId)
        throws (1: EThriftException.ncTException exp);

    /**
     * 删除自定义文档库
     *
     * @ret: 无返回
     * @throw EThriftException.ncTException
     */
    void EFAST_DeleteCustomDoc (1: ncTDeleteCustomDocParam info)
        throws (1: EThriftException.ncTException exp);

    /**
     * 获取自定义文档库总数
     * @param userId: 用户id
     * @ret: 自定义文档库总数
     * @throw EThriftException.ncTException
     */
    i32 EFAST_GetCustomDocCnt (1:string userId)
        throws (1: EThriftException.ncTException exp);

    /**
     * 根据文档库的对象id获取文档库信息
     *
     * @ret: 返回文档库信息
     * @throw EThriftException.ncTException
     */
    ncTCustomDocInfo EFAST_GetCustomDocByObjId (1: string objId)
        throws (1: EThriftException.ncTException exp);

    /**
     * 根据文档库id获取文档库信息
     *
     * @ret: 返回文档库信息
     * @throw EThriftException.ncTException
     */
    ncTCustomDocInfo EFAST_GetCustomDocByDocId (1: string docId)
        throws (1: EThriftException.ncTException exp);

    /**
     * 分页获取自定义文档库信息
     * @param start: 起始索引
     * @param limit: 获取文档数
     * @param userId: 用户id
     * @ret: 文档库信息
     * @throw EThriftException.ncTException
     */
    list<ncTCustomDocInfo> EFAST_GetCustomDocInfosByPage (1:i32 start, 2:i32 limit, 3:string userId)
        throws (1: EThriftException.ncTException exp);

    /**
     * 批量编辑文档库配额前检查空间是否足够
     * @ret:
     * @throw EThriftException.ncTException
     */
    void EFAST_CheckDocSpace(1: string userId, 2: list<string> docIds , 3: i64 quota) throws (1: EThriftException.ncTException exp);

     /**
     * 编辑文档库配额
     * @ret:
     * @throw EThriftException.ncTException
     */
    void EFAST_SetQuotaInfo(1: string userId, 2: string docId, 3: i64 quota) throws (1: EThriftException.ncTException exp);

    /**
     * 搜索用户自定义文档库信息
     */
    list<ncTCustomDocInfo> EFAST_SearchCustomDocInfos (1: ncTGetPageDocParam param) throws (1: EThriftException.ncTException exp);

    /**
     * 获取搜索用户自定义文档库信息条目数量
     */
    i32 EFAST_GetSearchCustomDocCnt (1: ncTGetPageDocParam param) throws (1: EThriftException.ncTException exp);

    /**
     * 设置文档库对象存储
     *
     * @throw EThriftException.ncTException
     */
    void EFAST_EditDocLibraryOSSId (1: string docId, 2: string ossId)
        throws (1: EThriftException.ncTException exp);

    /**
     * 创建批量新建自定义文档库任务
     *
     * @ret: 返回创建的任务id
     * @throw EThriftException.ncTException
     */
    string EFAST_BatchAddCustomDocs (1: ncTBatchAddCustomDocParam param)
        throws (1: EThriftException.ncTException exp);

    /**
     * 查询批量新建自定义文档库结果
     *
     * @ret: 返回创建的结果
     * @throw EThriftException.ncTException
     */
    ncTBatchAddCustomDocResult EFAST_GetBatchAddCustomDocsResult (1: string taskId)
        throws (1: EThriftException.ncTException exp);

    /**
     * 搜索用户自定义文档库信息 (组织管理员的结果中包含有所有者权限的文档库信息)
     */
    list<ncTCustomDocInfo> EFAST_SearchAvailableCustomDocInfos (1: ncTGetPageDocParam param) throws (1: EThriftException.ncTException exp);

    /**
     * 获取搜索用户自定义文档库信息条目数量 (组织管理员的结果中包含有所有者权限的文档库)
     */
    i32 EFAST_GetSearchAvailableCustomDocCnt (1: ncTGetPageDocParam param) throws (1: EThriftException.ncTException exp);

    /**
    * 修改自定义文档库的显示顺序
    */
    void EFAST_EditDisplayOrder (1: string docId, 2: string userId, 3: i32 displayOrder) throws (1: EThriftException.ncTException exp);

    /**
     * 新建归档文档库
     *
     * @ret: 返回创建成功后的id
     * @throw EThriftException.ncTException
     */
    // string EFAST_AddArchiveDoc (1: ncTAddArchiveDocParam info) throws (1: EThriftException.ncTException exp);

    /**
     * 编辑归档文档库
     *
     * @ret: 无返回
     * @throw EThriftException.ncTException
     */
    // void EFAST_EditArchiveDoc (1: ncTEditArchiveDocParam info) throws (1: EThriftException.ncTException exp);

    /**
     * 删除归档文档库
     *
     * @ret: 无返回
     * @throw EThriftException.ncTException
     */
    // void EFAST_DeleteArchiveDoc (1: ncTDeleteArchiveDocParam info) throws (1: EThriftException.ncTException exp);

    /**
     * 根据归档库id获取归档库信息
     *
     * @ret: 返回归档库信息
     * @throw EThriftException.ncTException
     */
    // ncTArchiveDocInfo EFAST_GetArchiveDocByDocId (1: string docId) throws (1: EThriftException.ncTException exp);

    /**
     * 获取归档文档库总数
     * @ret: 归档文档库总数
     * @throw EThriftException.ncTException
     */
    // i32 EFAST_GetArchiveDocCnt (1:string userId) throws (1: EThriftException.ncTException exp);

    /**
     * 分页获取归档文档库信息
     * @param start: 起始索引
     * @param limit: 获取文档数
     * @ret: 文档库信息
     * @throw EThriftException.ncTException
     */
    // list<ncTArchiveDocInfo> EFAST_GetArchiveDocInfosByPage (1:i32 start, 2:i32 limit, 3:string userId) throws (1: EThriftException.ncTException exp);

    /**
     * 搜索归档库信息
     */
    // list<ncTArchiveDocInfo> EFAST_SearchArchiveDocInfos(1: ncTGetPageDocParam param)throws (1: EThriftException.ncTException exp);

    /**
     * 获取搜索用户归档库信息条目数量
     */
    // i32 EFAST_GetSearchArchiveDocCnt(1: ncTGetPageDocParam param)throws (1: EThriftException.ncTException exp);

    /**
     * 搜索归档库信息(组织管理员的结果中包含有所有者权限的归档库信息)
     */
    // list<ncTArchiveDocInfo> EFAST_SearchAvailableArchiveDocInfos(1: ncTGetPageDocParam param)throws (1: EThriftException.ncTException exp);

    /**
     * 获取搜索用户归档库信息条目数量(组织管理员的结果中包含有所有者权限的归档库)
     */
    // i32 EFAST_GetSearchAvailableArchiveDocCnt(1: ncTGetPageDocParam param)throws (1: EThriftException.ncTException exp);

    /**
     * 移动个人文档
     *
     * @ret: 无返回
     * @throw EThriftException.ncTException
     */
    list<ncTCustomDocInfo> EFAST_MoveUserDoc (1: string adminId, 2: string userId, 3: string docId)
        throws (1: EThriftException.ncTException exp);

    /**
     * 移动个人文档（文档库恢复使用）
     *
     * @ret: 无返回
     * @throw EThriftException.ncTException
     */
    list<ncTCustomDocInfo> EFAST_MoveEntryDoc (1: string adminId, 2: string sourceDocId, 3: string targetDocId)
        throws (1: EThriftException.ncTException exp);

    /**
     * 删除个人文档
     *
     * @ret: 无返回
     * @throw EThriftException.ncTException
     */
    list<ncTCustomDocInfo> EFAST_DeleteUserDoc (1: string userId, 2: string deleterId)
        throws (1: EThriftException.ncTException exp);

    /**
     * 获取个人总配额，bytes
     *
     * @ret: 无返回
     * @throw EThriftException.ncTException
     */
    i64 EFAST_GetUserTotalQuota (1: string userId)
        throws (1: EThriftException.ncTException exp);

    /**
     * 获取个人已使用配额空间，bytes
     *
     * @ret: 无返回
     * @throw EThriftException.ncTException
     */
    i64 EFAST_GetUserUsedQuota (1: string userId)
        throws (1: EThriftException.ncTException exp);

    /**
     * 编辑个人总配额，bytes
     *
     * @ret: 无返回
     * @throw EThriftException.ncTException
     */
    void EFAST_EditUserTotalQuota  (1: string userId, 2: i64 totalQuotaBytes)
        throws (1: EThriftException.ncTException exp);

    /**
     * 检查用户是否有文档数据（包括个人文档）
     * @ret:
     * @throw EThriftException.ncTException
     */
    list<string> EFAST_GetAllUserDocById(1: string userId) throws(1: EThriftException.ncTException exp);

    /**
     * 检测用户显示名是否和自定义文档库、归档库名称冲突
     *
     * @ret:
     * @throw EThriftException.ncTException
     */
    bool EFAST_ConfictWithLibName (1: string name)
        throws (1: EThriftException.ncTException exp);

    /**
     * 获取用户配额空间信息
     * @ret:
     * @throw EThriftException.ncTException
     */
    ncTSpaceQuotaInfo EFAST_GetSpaceQuotaInfo(1: string userId) throws (1: EThriftException.ncTException exp);

    /**
     * 获取所有文档库类型名
     * @throw EThriftException.ncTException
     */
    list<string> EFAST_GetAllCustomDocTypeName ()
        throws (1: EThriftException.ncTException exp);

    /**
     * 根据用户id获取gns路径
     * @ret:
     * @throw EThriftException.ncTException
     */
    string EFAST_GetUserGns(1: string userId) throws (1: EThriftException.ncTException exp);

    /**
     * 根据自定义文档库docId和adminId恢复自定义文档库
     *
     * @ret:
     * @throw EThriftException.ncTException
     */
    void EFAST_SysRecycle_RestoreCustomDoc(1: string docId, 2: string name, 3: string adminId) throws (1: EThriftException.ncTException exp);

    /*
    * 根据文档的dicId恢复个人文档库
    *
    * @ret:
    * @throw EThriftException.ncTException
    */
    void EFAST_SysRecycle_RestoreUserDoc(1: string docId, 2: string responsiblePersonId) throws (1: EThriftException.ncTException exp);

    /**
     * 获取系统回收站的入口文档信息
     * @param start: 起始索引
     * @param limit: 获取文档数
     * @param searchKey: 搜索关键字, 为空时查找所有
     * @ret: 文档库信息
     * @throw EThriftException.ncTException
     */
    list<ncTSysRecycleEntryDocInfo> EFAST_SysRecycle_GetEntryDocInfos (1:i32 start, 2:i32 limit, 3:string searchKey) throws (1: EThriftException.ncTException exp);

    /**
     * 根据docId(cid)获取系统回收站的入口文档信息
     * @param docId: 文档id
     * @ret: 文档库信息
     * @throw EThriftException.ncTException
     */
    ncTSysRecycleEntryDocInfo EFAST_SysRecycle_GetEntryDocInfoByDocId (1:string docId) throws (1: EThriftException.ncTException exp);

    /**
     * 删除部门时通知efast删除文档库的关联部门
     *
     * @ret: 无返回
     * @throw EThriftException.ncTException
     */
    void EFAST_OnDeleteDepartment (1: list<string> departmentIds)
        throws (1: EThriftException.ncTException exp);

}
