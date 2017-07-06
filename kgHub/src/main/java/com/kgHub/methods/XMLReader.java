package com.kgHub.methods;


import java.util.ArrayList;
import java.util.List;
import org.dom4j.Document;
import org.dom4j.DocumentException;
import org.dom4j.Element;
import org.dom4j.io.SAXReader;

import com.kgHub.pojo.GraphNode;
import com.kgHub.pojo.GraphSearchServerConfig;
import com.kgHub.pojo.GraphServerConfig;

public class XMLReader {
	
	public ArrayList<GraphNode> graphList;
	
	public XMLReader(){
		this.graphList = new ArrayList<GraphNode>();
		 SAXReader reader = new SAXReader();
         try {
        	 Document doc = reader.read(this.getClass().getResourceAsStream("/graphServer.xml"));
        	 parseRootGraphServerConfig(doc.getRootElement());
         } catch (DocumentException e) {     
              e.printStackTrace();   
         }   
	}
	
	
	public GraphServerConfig parseGraphServerConfig(Element e){
		System.out.println("parseGraphServerConfig");
		GraphServerConfig server=null;
		if(e.getName().equals("GraphServer")==true){
			String state=e.attribute("state").getText();
			if(state.equals("on")){
				GraphServerConfig temp=new GraphServerConfig();
				temp.setPassword(e.attribute("password").getText());
				temp.setType(e.attribute("type").getText());
				temp.setURL(e.attribute("URL").getText());
				temp.setUserName(e.attribute("userName").getText());
				temp.setState(true);
				server=temp;
			}
		}
		return server;
	}
	
	public GraphSearchServerConfig parseGraphSearchServerConfig(Element e){
		System.out.println("parseGraphSearchServerConfig");
		GraphSearchServerConfig server=null;
		if(e.getName().equals("GraphSearchServer")==true){
			String state=e.attribute("state").getText();
			if(state.equals("on")){
				GraphSearchServerConfig temp=new GraphSearchServerConfig();
				temp.setEngineClass(e.attribute("engineClass").getText());
				temp.setEnterPath(e.attribute("enterPath").getText());
				temp.setHost(e.attribute("host").getText());
				temp.setScheme(e.attribute("scheme").getText());
				temp.setState(true);
			}
		}
		return server;
	}
	
	public void parseGraphNode(Element e,String typeID){
		System.out.println("parseGraphNode");
		@SuppressWarnings("unchecked")
		List<Element> elements=e.elements();
		for(Element iter:elements){
			if(iter.getName().equals("GraphNode")){
				String active=iter.attribute("active").getText();
				if(active.equals("true")){
					GraphNode graphNode=new GraphNode();
					graphNode.setActive(true);
					graphNode.setId(iter.attribute("id").getText());
					graphNode.setName(iter.attribute("name").getText());
					graphNode.setTypeID(typeID);
					
					ArrayList<GraphServerConfig> servers=new ArrayList<GraphServerConfig>();
					ArrayList<GraphSearchServerConfig> searchServers=new ArrayList<GraphSearchServerConfig>();
					
					@SuppressWarnings("unchecked")
					List<Element> elements1=iter.elements();
					for(Element iter1:elements1){
						if(iter1.getName().equals("GraphServers")){
							@SuppressWarnings("unchecked")
							List<Element> elements2=iter1.elements();
							for(Element iter2:elements2){
								servers.add(parseGraphServerConfig(iter2));
							}
						}
						if(iter1.getName().equals("GraphSearchServers")){
							@SuppressWarnings("unchecked")
							List<Element> elements2=iter1.elements();
							for(Element iter2:elements2){
								searchServers.add(parseGraphSearchServerConfig(iter2));
							}
						}
					}
					
					graphNode.setServers(servers);
					graphNode.setSearchServers(searchServers);
					graphList.add(graphNode);
				}
			}
		}
	}
	
	public void parseGraphTypeNode(Element e){
		System.out.println("parseGraphTypeNode");
		String typeID=e.attribute("id").getText();
		@SuppressWarnings("unchecked")
		List<Element> elements=e.elements();
		for(Element iter:elements){
			if(iter.getName().equals("GraphListNode")){
				parseGraphNode(iter, typeID);
			}
		}
	}
	
	public void parseRootGraphServerConfig(Element e){
		@SuppressWarnings("unchecked")
		List<Element> elements=e.elements();
		for(Element iter:elements){
			if(iter.getName().equals("GraphTypeNode")){
				parseGraphTypeNode(iter);
			}
		}
	}
}
