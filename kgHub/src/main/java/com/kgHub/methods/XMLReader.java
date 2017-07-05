package com.kgHub.methods;


import java.util.ArrayList;
import java.util.HashMap;
import java.util.Iterator;
import java.util.List;
import java.util.Map;

import org.dom4j.Attribute;
import org.dom4j.Element;

public class XMLReader {
	
    public Combinement SpecifiedMethod(Element element, Element FatherNode){
    	Map<String, Object> map=new HashMap<String, Object>();
    	List list=new ArrayList();
    	if(element.getName().equals("GraphServerConfig")){
    		List<Element> elements=element.elements();
    		List temp=new ArrayList<>();
    		for(Element ele:elements){
    			temp=SpecifiedMethod(ele,null).list;
    			for(int i=0;i<temp.size();i++){
    				list.add(temp.get(i));
    			}
    		}
    	}
    	else if(element.getName().equals("GraphTypeNode")){
    		List<Element> elements=element.elements();
    		List temp=new ArrayList<>();
    		if(element.attribute("active").getText().equals("false")==true){
    			Combinement combinement=new Combinement(map, list);
    			return combinement;
    		}
    		for(Element ele:elements){
    			temp=SpecifiedMethod(ele, element).list;
    			for(int i=0;i<temp.size();i++){
    				list.add(temp.get(i));
    			}
    		}
    	}
    	else if(element.getName().equals("GraphListNode")){
    		List<Element> graphnodes=element.elements();
    		for(Element ele:graphnodes){
    			list.add(SpecifiedMethod(ele, FatherNode).map);
    		}
    	}
    	else if(element.getName().equals("GraphNode")){
    		if(element.attribute("active").getText().equals("false")==true){
    			Combinement combinement=new Combinement(map, list);
    			return combinement;
    		}
    		List<Attribute> SonAttr=element.attributes();
    		List<Attribute> FatherAttr=FatherNode.attributes();
    		List<Element> elements=element.elements();
    		for(Attribute attr:SonAttr){
    			if(attr.getName().equals("active")==false)	map.put(attr.getName(),attr.getValue());
    		}
    		for(Attribute attr:FatherAttr){
    			if(attr.getName().equals("active")==false)	map.put("Type"+attr.getName(),attr.getValue());
    		}
    		for(Element ele:elements){
    			map.put(ele.getName(),SpecifiedMethod(ele,null).list);
    		}
    	}
    	else if(element.getName().equals("GraphServers")||element.getName().equals("GraphSearchServers")){
    		List<Element> elements=element.elements();
    		for(Element ele:elements){
    			if(ele.attribute("state").getText().equals("off")==true){
    				continue;
    			}
    	   		Map<String,Object> temp=new HashMap<>();
    			for(Iterator it=ele.attributeIterator();it.hasNext();){
    				Attribute attr = (Attribute) it.next();
    				if(attr.getName().equals("state")==false)	temp.put(attr.getName(), attr.getValue());
    				//System.out.println(attr.getName()+" "+attr.getValue());
    			}
    			list.add(temp);
    		}
    	}
    	else{
    		System.out.println("unknown type");;
    	}
    	Combinement combinement=new Combinement(map, list);
    	return combinement;
    }
	
    public List XMLRead(Element root){
    	return SpecifiedMethod(root,null).list;
    }
    
	static class Combinement{
		Map<String,Object> map;
		List list;
		
		public Combinement(Map<String,Object> map,List list) {
			// TODO Auto-generated constructor stub
			this.map=map;
			this.list=list;
		}
	}
}
