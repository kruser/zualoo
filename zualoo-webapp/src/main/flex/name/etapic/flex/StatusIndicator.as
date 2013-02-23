package name.etapic.flex
{
	import name.etapic.gelt.admin.Status;
	
	/**
	 * Store a label in a static place so the contents of it can be manipulated
	 * across other classes.
	 */
	public class StatusIndicator
	{
		public static var status:Status;
		
		/**
		 * Change the message in the status label
		 */
		public static function set statusMessage(label:String):void
		{
			if (status != null)
			{
				status.statusLabel.text = label;	
				status.visible = true;
			}
		}
		
		/**
		 * Get the current message in the status label
		 */
		public static function get statusMessage():String
		{
			if (status != null)
			{
				return status.statusLabel.text;
			}
			else
			{
				return 'Label not yet set up';
			}
		}
		
		/**
		 * Hide the status label.  This can be called when
		 * any action is complete.
		 */ 
		public static function hideStatus():void
		{
			if (status != null)
			{
				status.visible = false;
			}
		}
	}
}