<?xml version="1.0" encoding="UTF-8"?>
<tileset version="1.10" tiledversion="1.11.0" name="props" tilewidth="138" tileheight="140" tilecount="2" columns="0" objectalignment="bottomleft">
 <grid orientation="orthogonal" width="1" height="1"/>
 <tile id="0" type="prop">
  <properties>
   <property name="prop" value="desk"/>
   <property name="anchorX" type="float" value="51"/>
   <property name="anchorY" type="float" value="72"/>
   <property name="solid" type="bool" value="true"/>
   <property name="occlusionClass" value="tall"/>
   <property name="occupantPolicy" value="y_sort"/>
  </properties>
  <image source="images/desk.png" width="102" height="73"/>
  <objectgroup draworder="index" id="2">
   <object id="1" name="footprint" type="footprint" x="-5" y="44" width="112" height="28"/>
  </objectgroup>
 </tile>
 <tile id="1" type="prop">
  <properties>
   <property name="prop" value="shelf"/>
   <property name="anchorX" type="float" value="69"/>
   <property name="anchorY" type="float" value="139"/>
   <property name="solid" type="bool" value="true"/>
   <property name="occlusionClass" value="tall"/>
   <property name="occupantPolicy" value="y_sort"/>
  </properties>
  <image source="images/shelf.png" width="138" height="140"/>
  <objectgroup draworder="index" id="2">
   <object id="1" name="footprint" type="footprint" x="7.5" y="116" width="123" height="23"/>
  </objectgroup>
 </tile>
</tileset>
