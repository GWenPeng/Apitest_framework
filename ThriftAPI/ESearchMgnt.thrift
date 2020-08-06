/*********************************************************************************
ESearchMgnt.thrift:
    全文检索管理接口文件
    Copyright (c) Eisoo Software, Inc.(2012 - 2017), All rights reserved.

Purpose:
    此文件定义全文检索管理接口

Author:
    Chen Hao (chen.hao01@eisoo.com)

Creating Time:
    2013-12-27

*********************************************************************************/

include "EThriftException.thrift"

/**
 * 端口号
 */
const i32 NCT_ESM_PORT = 32066

struct ncTUserDictInfo {
    1: string id;    // 词库id
    2: string name;  // 词库文件名
    3: i64 upTime;   // 词库上传时间
}

// 错误码
enum ncTESearchMgntError {
    NCT_DB_OPERATE_FAILED = 10001,                              // 数据库执行失败
    NCT_UNKNOWN_ERROR = 10002,                                  // 未知错误

    NCT_CANT_ENABLE_KEYSCAN_CAUSE_FULLTEXT_INDEX_NOT_INSTALLED = 20001,     // 全文检索尚未安装，无法开启非法内容管控
    NCT_INVALID_USER_DICT_FNAME = 200002,       // 非法的词库文件名称
    NCT_INVALID_USER_DICT_FCONTENT = 200003,    // 非法的词库内容
    NCT_RENAMED_LENGTH_EXCEEDS = 200004,        // 重名处理后，长度超过255
    NCT_USER_DICT_NOT_EXISTS = 200005,          // 词库不存在或者已被删除
    NCT_EXCEED_MAX_DICT_COUNT = 200006,         // 词库文件数量不能超过32个
    NCT_EXCEED_FCONTENT_LENTH = 200007,         // 词库文件大小不能超过4M
    NCT_CANT_ENABLE_KEYSCAN_CAUSE_NO_USER_DICT = 200008,                    // 未上传任何词库，无法开启非法内容管控
    NCT_HAVE_NO_ACTIVED_LICENSE =  200009,      // 无授权码或授权码未激活

    NCT_SUMMARY_CONF_NO_SUCH_FIELD = 200101,                    // 摘要配置中没有这样的字段
    NCT_SUMMARY_DOES_NOT_SUPPORT_THIS_LANGUAGE = 200102,        // 摘要不支持该语言
    NCT_SIZE_LESS_THAN_ZERO = 200103,                           // 需要进行缩略的图片大小小于0
}

enum ncTKeyScanTaskFlag {
    NCT_ILLEGALCONTENT = 1,                              // 非法内容扫描
    NCT_WORDSCAN = 2,                                    // 关键字扫描
}

service ncTESearchMgnt {
    /**
     * 修改全文检索探测间隔
     *
     * @interval: 时间间隔，单位 秒
     */
    void SetIndexInterval(1: i32 interval) throws (1: EThriftException.ncTException exp)

    /**
     * 查询全文检索服务（eftsearch）的状态
     *
     * @return: True为服务处于启动状态，False为服务处于停止状态。
     */
    bool GetServiceStatus() throws (1: EThriftException.ncTException exp)

    /**
     * 检查是否启用非法内容管控
     *
     * @return: True表示已经启用 False表示未启用
     */
    bool Keyscan_IsEnabled() throws (1: EThriftException.ncTException exp)

    /**
     * 设置是否启用非法内容管控
     *
     * @param enable: True表示启用 False表示关闭
     */
    void Keyscan_SetEnabled(1: bool enable) throws (1: EThriftException.ncTException exp)

    /**
     * 添加用户自定义词库，失败会以各种异常抛出
     *
     * @param fname: 词库文件名
     * @param fcontent: 词库内容
     */
    ncTUserDictInfo Keyscan_AddUserDict(1: string fname, 2: string fcontent) throws (1: EThriftException.ncTException exp)

    /**
     * 删除用户自定义词库
     *
     * @param userid: 词库id
     */
    void Keyscan_DelUserDict(1: string dictid) throws (1: EThriftException.ncTException exp)

    /**
     * 获取所有自定义词库信息
     *
     * @return: 自定义词库信息
     */
    list<ncTUserDictInfo> Keyscan_GetAllUserDictInfo() throws (1: EThriftException.ncTException exp)

    /**
     * 获取自定义词库内容
     *
     * @return: 自定义词库内容
     */
    string Keyscan_GetUserDictContent(1: string dictid) throws (1: EThriftException.ncTException exp)

    /**
     * 获取默认词库内容
     *
     * @return: 默认词库内容
     */
    string Keyscan_GetDefUserDictContent() throws (1: EThriftException.ncTException exp)

    /**
     * 开始全量扫描任务，如果有任务，则终止已有的任务
     *
     * @param taskFlag: 1：非法检测 2：关键字扫描 3：所有
     * @return:
     */
    i64 FullScan_Begin(1: i32 taskFlag) throws (1: EThriftException.ncTException exp)

    /**
     * 终止掉当前的扫描任务
     *
     * @return:
     */
    void FullScan_Stop() throws (1: EThriftException.ncTException exp)

    /**
     * 查询全量扫描任务状态
     *
     * @return: 1: 未开始 2：进行中 3. 已完成
     */
    i64 FullScan_Stat() throws (1: EThriftException.ncTException exp)

    /**
     * 检查是否启用非法内容检测
     *
     * @return: True表示已经启用 False表示未启用
     */
    bool IllegalCtrl_IsEnabled() throws (1: EThriftException.ncTException exp)

    /**
     * 设置是否启用非法内容检测
     *
     * @param enable: True表示启用 False表示关闭
     */
    void IllegalCtrl_SetEnabled(1: bool enable) throws (1: EThriftException.ncTException exp)

    /**
     * 获取功能授权码状态
     *
     * @return: True表示已经激活 False表示未激活
     */
    bool Analysis_LicenseState() throws (1: EThriftException.ncTException exp)

    /**
     * 设置摘要功能状态
     *
     * @param field: enable_pic_summary             图片摘要
     *               enable_pic_tag_and_summary     图片标签和摘要（打开此开关是获取图片摘要的前提）
     *               enable_text_summary            文档摘要
     *
     * @param enable: True表示启用 False表示关闭
     */
    void Summary_SetStatus(1: string field, 2: bool enable) throws (1: EThriftException.ncTException exp)

    /**
     * 获取摘要功能状态
     *
     * @param field: 可选enable_pic_summary, enable_pic_tag_and_summary, enable_text_summary
     * @return: True表示启用 False表示关闭
     */
    bool Summary_GetStatus(1: string field) throws (1: EThriftException.ncTException exp)

    /**
     * 设置图片摘要功能支持的语言
     *
     * @param language: 图片摘要功能支持的语言
     */
    void Summary_SetPicSummaryTagLanguage(1: string language) throws (1: EThriftException.ncTException exp)

    /**
     * 获取图片摘要功能支持的语言
     *
     * @return: 图片摘要功能支持的语言
     */
    string Summary_GetPicSummaryTagLanguage() throws (1: EThriftException.ncTException exp)

    /**
     * 设置图片需要进行缩略的大小
     *
     * @param size: 图片需要进行缩略的大小
     */
    void Summary_SetNeedThumbnailSize(1: i64 size) throws (1: EThriftException.ncTException exp)

    /**
     * 获取图片需要进行缩略的大小
     *
     * @param size: 图片需要进行缩略的大小
     */
    i64 Summary_GetNeedThumbnailSize() throws (1: EThriftException.ncTException exp)
}