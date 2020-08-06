/*********************************************************************************

ERomote.thrift:
    定义 AT测试远程接口定义文件	
    Copyright (c) Eisoo Software, Inc.(2012 - ), All rights reserved.

Purpose:
    此接口文件定义 AT测试远程接口。

Author:
    zhong.hua(zhong.hua@eisoo.com)
	
Creating Time:
    2012-12-5
    
*********************************************************************************/

include "EThriftException.thrift"

typedef i32 int32
typedef i64 int64

const int32 NCT_ERomote_PORT = 9091

typedef list<string> ncRemoteList
typedef list<string> ncTransferList

service ncTERemote {

	/**
	 *
	 * 执行客户传送过来的命令
	 *
	 * @throw EThriftException.ncTException: 1.获取失败
	 *
	 *
	 */
	 void run_commands(1: ncRemoteList commandline)
	              throws (1: EThriftException.ncTException exp)
				  
	 void run_commands_return(1: ncRemoteList commandline)
	              throws (1: EThriftException.ncTException exp)
	 
	 void Transfer(1: ncTransferList file,2: string ip,3: int32 port )
	              throws (1:EThriftException.ncTException exp) 
}