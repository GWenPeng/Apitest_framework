/*******************************************************************************************
ECNJY.thrift
    Copyright (c) Eisoo Software, Inc.(2013 - 2014), All rights reserved

Purpose:
    ECNJY 数据管理接口.
    提供 GNS 管理对象的增删查等.

Author:
    Liu Lang (liu.lang@eisoo.com)

Creating Time:
    2013-05-13
*******************************************************************************************/

include "EThriftException.thrift"

/**
 * 端口号
 */
const i32 NCT_ECNJY_PORT = 9067

/**
 * 同步进度返回值
 */
struct ncTECNJYProgress {
    1: required i64 hasfininum,
    2: required i64 notfininum,
    3: required i64 totalsize,
}

/**
 * 获取同步账户和密码
 */
struct ncTECNJYPwd {
    1: required string partnerid,
    2: required string key,
}

/**
 * 获取同步机制
 */
struct ncTECNJYMechanism {
    1: required i32 day,
    2: required i32 hour,
    3: required i32 min,
    4: required i32 sec,
}

/**
 * 错误日志
 * type：0为同步成功日志，1为同步失败日志
 */
struct ncTECNJYLog {
    1: required i64 id,
    2: required i64 btime,
    3: required i64 etime,
    4: required string description,
    5: required i32 type,
}

/**
 * GNS 对象集
 */
struct ncTECNJYLogSet {
    1: required list<ncTECNJYLog> cnjyLogs,    // 日志对象集
}

/**
 * ECNJY 管理服务接口
 */
service ncTECNJY {

    /**
     * 是否已经初始化了21世纪教育网同步器
     *
     * @return 安装返回true，未安装返回false
     * @throw 转抛内部调用异常
     */
    bool HasInit ()
                  throws (1: EThriftException.ncTException exp),
                
    /**
     * 获取安装节点的IP
     *
     * @return 安装节点的IP,如果未安装则返回空
     * @throw 转抛内部调用异常
     */
    string GetIp ()
                  throws (1: EThriftException.ncTException exp),
    
    /**
     * 获取21世纪教育网账户
     *
     * @return 账户和密码
     * @throw 转抛内部调用异常
     */
    ncTECNJYPwd GetCNJYPassWord ()
                                 throws (1: EThriftException.ncTException exp),
    
    /**
     * 设置同步机制
     *
     * @param day:    每隔day天，范围[1,7]
     * @param hour:    每天的hour时，范围[0,23]
     * @param min:    每时的min分，范围[0,59]
     * @param sec:  每分的sec秒，范围[0,59]
     * @throw 转抛内部调用异常
     */            
    void SetSyncMechanism (1: i32 day, 2: i32 hour, 3: i32 min, 4: i32 sec)
                           throws (1: EThriftException.ncTException exp),
    
    /**
     * 获取同步机制
     *
     * @return 同步机制
     * @throw 转抛内部调用异常
     */
    ncTECNJYMechanism GetSyncMechanism ()
                                        throws (1: EThriftException.ncTException exp),
    
    /**
     * 发起增量立即同步
     *
     * @throw 转抛内部调用异常
     */
    void DeltaSyncNow ()
                       throws (1: EThriftException.ncTException exp),

    /**
     * 发起套餐变更立即同步
     *
     * @throw 转抛内部调用异常
     */
    void ScanSyncNow ()
                      throws (1: EThriftException.ncTException exp),
                
    /**
     * 查询同步状态
     *
     * @return 是否正在同步中，是返回true，否返回false
     * @throw 转抛内部调用异常
     */
    bool SyncStatus ()
                     throws (1: EThriftException.ncTException exp),
                
    /**
     * 查看同步进度
     *
     * @return 同步进度，不在同步状态默认为-1，-1，-1
     * @throw 转抛内部调用异常
     */
    ncTECNJYProgress GetProgress ()
                                  throws (1: EThriftException.ncTException exp),
    
    /**
     * 查看同步日志
     *
     * @param limit:   每次返回条数
     * @param maxid:   等于0，则取最大的limit条；小于0抛错，抛错；大于0，获取小于maxid的最大limit条日志
     * @param type:    为0，取成功的日志；为1，取失败的日志；其他则取所有日志
     * @return 最大的同步日志(按顺序排序，大的在前面，小的在后面)
     * @throw 转抛内部调用异常
     */
    ncTECNJYLogSet GetMaxSyncLogs (1: i32 limit, 2: i64 maxid, 3: i32 type)
                                   throws (1: EThriftException.ncTException exp),
}
