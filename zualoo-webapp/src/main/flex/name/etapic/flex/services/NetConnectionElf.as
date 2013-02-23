package name.etapic.flex.services
{
	import flash.events.NetStatusEvent;
	import flash.events.SecurityErrorEvent;
	import flash.net.NetConnection;
	import flash.net.Responder;
	
	import lt.uza.utils.Global;
	
	public class NetConnectionElf
	{
		public static var connection:NetConnection = null;
		
		// The URL to use for the remoting gateway when testing locally in the
		// Flash IDE or the Standalone Flash Player. Change this according to your needs.
		public static var localhost:String = "http://localhost:8080";
		private static var localGatewayURL:String = localhost + "/gateway"
		
		public function NetConnectionElf()
		{
		}
		
        public static function call(serviceName:String, callback:Function, ...args):void
        {
        	var connection:NetConnection = getConnection();
        	var responder:Responder = new Responder(callback, faultHandler);
        	args.unshift(responder);
        	args.unshift(serviceName);
        	connection.call.apply(connection, args);
        }

        private static function getConnection():NetConnection
        {
        	if (connection == null)
        	{
        		connection = new NetConnection();
        		var app:Global = Global.getInstance();
				var url:String = (app.isLocal) ? localGatewayURL : app.baseURL + "/gateway";					
				
				connection.addEventListener(NetStatusEvent.NET_STATUS, netStatusHandler);
				connection.addEventListener(SecurityErrorEvent.SECURITY_ERROR, securityErrorHandler);
				
				connection.connect(url);		
        	}
        	return connection;
        }
        
        private static function faultHandler(fault:Object):void
        {
        	trace(fault);
        }
        
        private static function netStatusHandler(event:NetStatusEvent):void
		{
			trace ("[netStatusHandler] " + event.info.level + ": " + event.info.code);
		}
		
        private static function securityErrorHandler(event:SecurityErrorEvent):void 
		{
            trace("[securityErrorHandler] " + event);
        }
	}
}