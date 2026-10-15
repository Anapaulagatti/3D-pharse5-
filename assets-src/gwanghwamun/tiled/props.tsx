<?xml version="1.0" encoding="UTF-8"?>
<tileset version="1.10" tiledversion="1.11.0" name="props" tilewidth="461" tileheight="340" tilecount="12" columns="0" objectalignment="bottomleft">
 <grid orientation="orthogonal" width="1" height="1"/>
 <tile id="0" type="prop">
  <properties>
   <property name="prop" value="bench"/>
   <property name="anchorX" type="float" value="37"/>
   <property name="anchorY" type="float" value="51"/>
   <property name="solid" type="bool" value="true"/>
   <property name="occlusionClass" value="tall"/>
  </properties>
  <image source="images/bench.png" width="75" height="52"/>
  <objectgroup draworder="index" id="2">
   <object id="1" name="footprint" type="footprint" x="4" y="35" width="66" height="16"/>
  </objectgroup>
 </tile>
 <tile id="1" type="prop">
  <properties>
   <property name="prop" value="bridge"/>
   <property name="anchorX" type="float" value="69"/>
   <property name="anchorY" type="float" value="55"/>
   <property name="solid" type="bool" value="false"/>
   <property name="occlusionClass" value="tall"/>
  </properties>
  <image source="images/bridge.png" width="138" height="56"/>
 </tile>
 <tile id="2" type="prop">
  <properties>
   <property name="prop" value="gate"/>
   <property name="anchorX" type="float" value="230"/>
   <property name="anchorY" type="float" value="339"/>
   <property name="solid" type="bool" value="true"/>
   <property name="occlusionClass" value="tall"/>
  </properties>
  <image source="images/gate.png" width="461" height="340"/>
  <objectgroup draworder="index" id="2">
   <object id="1" name="footprint" type="footprint" x="35" y="257" width="390" height="82"/>
  </objectgroup>
 </tile>
 <tile id="3" type="prop">
  <properties>
   <property name="prop" value="ginkgo"/>
   <property name="anchorX" type="float" value="102"/>
   <property name="anchorY" type="float" value="213"/>
   <property name="solid" type="bool" value="true"/>
   <property name="occlusionClass" value="tall"/>
  </properties>
  <image source="images/ginkgo.png" width="204" height="214"/>
  <objectgroup draworder="index" id="2">
   <object id="1" name="footprint" type="footprint" x="91" y="201" width="22" height="12"/>
  </objectgroup>
 </tile>
 <tile id="4" type="prop">
  <properties>
   <property name="prop" value="hall"/>
   <property name="anchorX" type="float" value="137"/>
   <property name="anchorY" type="float" value="213"/>
   <property name="solid" type="bool" value="true"/>
   <property name="occlusionClass" value="tall"/>
  </properties>
  <image source="images/hall.png" width="274" height="214"/>
  <objectgroup draworder="index" id="2">
   <object id="1" name="footprint" type="footprint" x="44.5" y="155" width="185" height="58"/>
  </objectgroup>
 </tile>
 <tile id="5" type="prop">
  <properties>
   <property name="prop" value="jars"/>
   <property name="anchorX" type="float" value="32"/>
   <property name="anchorY" type="float" value="52"/>
   <property name="solid" type="bool" value="true"/>
   <property name="occlusionClass" value="tall"/>
  </properties>
  <image source="images/jars.png" width="65" height="53"/>
  <objectgroup draworder="index" id="2">
   <object id="1" name="footprint" type="footprint" x="6" y="32" width="52" height="20"/>
  </objectgroup>
 </tile>
 <tile id="6" type="prop">
  <properties>
   <property name="prop" value="lantern"/>
   <property name="anchorX" type="float" value="26"/>
   <property name="anchorY" type="float" value="91"/>
   <property name="solid" type="bool" value="true"/>
   <property name="occlusionClass" value="tall"/>
  </properties>
  <image source="images/lantern.png" width="52" height="92"/>
  <objectgroup draworder="index" id="2">
   <object id="1" name="footprint" type="footprint" x="18" y="81" width="16" height="10"/>
  </objectgroup>
 </tile>
 <tile id="7" type="prop">
  <properties>
   <property name="prop" value="pavilion"/>
   <property name="anchorX" type="float" value="121"/>
   <property name="anchorY" type="float" value="177"/>
   <property name="solid" type="bool" value="true"/>
   <property name="occlusionClass" value="tall"/>
  </properties>
  <image source="images/pavilion.png" width="242" height="178"/>
  <objectgroup draworder="index" id="2">
   <object id="1" name="footprint" type="footprint" x="30" y="123" width="182" height="54"/>
  </objectgroup>
 </tile>
 <tile id="8" type="prop">
  <properties>
   <property name="prop" value="planter"/>
   <property name="anchorX" type="float" value="28"/>
   <property name="anchorY" type="float" value="43"/>
   <property name="solid" type="bool" value="true"/>
   <property name="occlusionClass" value="tall"/>
  </properties>
  <image source="images/planter.png" width="56" height="44"/>
  <objectgroup draworder="index" id="2">
   <object id="1" name="footprint" type="footprint" x="-3" y="26" width="62" height="17"/>
  </objectgroup>
 </tile>
 <tile id="9" type="prop">
  <properties>
   <property name="prop" value="sejong"/>
   <property name="anchorX" type="float" value="61"/>
   <property name="anchorY" type="float" value="135"/>
   <property name="solid" type="bool" value="true"/>
   <property name="occlusionClass" value="tall"/>
  </properties>
  <image source="images/sejong.png" width="123" height="136"/>
  <objectgroup draworder="index" id="2">
   <object id="1" name="footprint" type="footprint" x="23" y="100" width="76" height="35"/>
  </objectgroup>
 </tile>
 <tile id="10" type="prop">
  <properties>
   <property name="prop" value="tree"/>
   <property name="anchorX" type="float" value="94"/>
   <property name="anchorY" type="float" value="195"/>
   <property name="solid" type="bool" value="true"/>
   <property name="occlusionClass" value="tall"/>
  </properties>
  <image source="images/tree.png" width="189" height="196"/>
  <objectgroup draworder="index" id="2">
   <object id="1" name="footprint" type="footprint" x="82" y="181" width="24" height="14"/>
  </objectgroup>
 </tile>
 <tile id="11" type="prop">
  <properties>
   <property name="prop" value="wall"/>
   <property name="anchorX" type="float" value="67"/>
   <property name="anchorY" type="float" value="55"/>
   <property name="solid" type="bool" value="true"/>
   <property name="occlusionClass" value="tall"/>
  </properties>
  <image source="images/wall.png" width="134" height="56"/>
  <objectgroup draworder="index" id="2">
   <object id="1" name="footprint" type="footprint" x="11" y="37" width="112" height="18"/>
  </objectgroup>
 </tile>
</tileset>
