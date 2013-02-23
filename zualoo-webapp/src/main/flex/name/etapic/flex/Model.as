package name.etapic.flex
{
	import name.etapic.flex.services.NetConnectionElf;
	
	public class Model
	{
		public static var loginURL:String = null;
		public static var logoutURL:String = null;
		public static var user:Object = null;
		public static var householdId:int = -1;
		public static var auth:Boolean = false;
		
		[Bindable]
		public static var myStores:Array;
		
		[Bindable]
		public static var storeSections:Array;
		
		private static var whenStoresChange:Function;
		
		public static function init():void
		{			
		}
			
		
		public static function userLoginResponse(result:Object):void
		{
			auth = result.auth;
			loginURL = result.login;
			logoutURL = result.logout;
						
			if (result.user != null)
			{
				user = result.user;
			}
		}
		
		public static function userGetUrlsResponse(result:Object):void
		{
			loginURL = result.login;
			logoutURL = result.logout;	
		}
		
		public static function setMyStores(stores:Array):void
		{
			myStores = stores;
			myStores.sort(storeSort);
			if (whenStoresChange != null)
			{
				whenStoresChange();
			}
		}
		
		public static function set myStoresChange(callback:Function):void
		{
			whenStoresChange = callback;
		}
		
		private static function storeSort(store1:Object, store2:Object):int
		{
			return store1[1].retail_store.name.localeCompare(store2[1].retail_store.name);	
		}
	}
}