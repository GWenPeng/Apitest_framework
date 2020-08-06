/*
 * Logger.thrift:
 *    日志模块接口文件
 *    Copyright (c) Eisoo Software, Inc.(2012 - ), All rights reserved.
 *
 *Purpose:
 *    提供日志接口。
 *
 *Author:
 *    Yeyouqun (ye.youqun@eisoo.com)
 *
 *Creating Time:
 *    2013.1.12
 *
 */


include "EThriftException.thrift"

const i32 NCT_INFOWORKS_LOGGER_PORT = 9090

enum ncTLogType {
    LT_INFO,
    LT_WARNNING,
    LT_ERROR,
    LT_OPERATION,
	LT_DEBUG,
}

struct ncTLogItem {
    1:required string       owner,      // 所属模块。
    2:required ncTLogType   log_type,   // Log 类型，见 ncTLogType。
    3:required string       log_mesg,   // Log 消息数据。
    4:required string       filename,   // 写 Log 的文件名。
    5:required i32          line,       // 写 Log 所在的行号。
    6:required i32      	time,          // Log 记录时间 时间为本地时间  格式为时间戳：1389766524.92
    7:optional string       host,       // Log 所在的主机名，若AddLog时未填写则默认使用localhost
}

service ncTEInfoworksLoggerService {
    /**
     * 记入 Log 信息
     * 当日志记录的量超过一定的阈值时，会对日志进行裁切，丢弃最早记录的日志。
     * @param entry         日志内容
     *    该接口不抛出异常!!
     */
    oneway void Log_AddLog (1:ncTLogItem entry)
}
