/*********************************************************************************
EKeyScanMonitor.thrift:
    Copyright (c) Eisoo Software, Inc.(2012 - 2017), All rights reserved.

Purpose:
    非法内容扫描任务管理，运行在eindexdaemon，用来响应终止任务的请求

Author:
    zou.yongbo@eisoo.com

Creating Time:
    2017-06-22
*********************************************************************************/
include "EThriftException.thrift"

/**
 * 端口号
 */
const i32 NCT_KSM_PORT = 9068


service ncTEKeyScanMonitor {
    /**
     * 终止掉当前的扫描任务
     *
     * @return:
     */
    void Keyscan_StopFullScan() throws (1: EThriftException.ncTException exp)


    /**
     * 修改全文检索探测间隔
     *
     * @interval: 时间间隔，单位 秒
     */
    void SetIndexInterval(1: i32 interval) throws (1: EThriftException.ncTException exp)
}
