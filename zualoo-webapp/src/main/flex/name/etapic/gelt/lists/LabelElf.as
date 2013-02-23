package name.etapic.gelt.lists
{
	public class LabelElf
	{
		public function LabelElf()
		{
		}
		
		public static function itemStoreSection(item:Object, other:Object):String
		{
			return item[1].item_description.store_section.name;
		}
		
		public static function storeSection(section:Object):String
		{
			return section[1].name;
		}
			
		public static function itemDescriptionLabel(item:Object, other:Object):String
		{
			return item[1].item_description.description;
		}
		
		/**
		 * The label for ItemDescription objects.... not yet part of a list
		 */
		public static function storeItemDescriptionLabel(item:Object, other:Object):String
		{
			return item[1].description;
		}
		
		public static function itemQuantity(item:Object, other:Object):String
		{
			return item[1].quantity;
		}
		
		public static function storeNameLabel(store:Object, other:Object):String
		{
			return store[1].name;
		}
		
		public static function householdStoreLabel(store:Object):String
		{
			return store[1].retail_store.name;
		}
		
		public static function householdStoreLabelDatagrid(store:Object, other:Object):String
		{
			return householdStoreLabel(store);
		}
	}
}