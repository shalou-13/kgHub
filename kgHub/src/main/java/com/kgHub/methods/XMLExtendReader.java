package com.kgHub.methods;

import java.util.ArrayList;
import java.util.List;

import org.dom4j.Document;
import org.dom4j.DocumentException;
import org.dom4j.Element;
import org.dom4j.io.SAXReader;

import com.alibaba.fastjson.JSON;
import com.kgHub.pojo.GraphNode;
import com.kgHub.pojo.GraphSearchServerConfig;
import com.kgHub.pojo.GraphTypeNode;


public class XMLExtendReader {
	
	public ArrayList<GraphNode> graphList;
	public ArrayList<GraphTypeNode> graphTypeList;
	
	public XMLExtendReader(){
		this.graphList = new ArrayList<GraphNode>();
		 SAXReader reader = new SAXReader();
         try {
        	 Document doc = reader.read(this.getClass().getResourceAsStream("/graphExtendServer.xml"));
        	 parseGraphServerConfig(doc.getRootElement());
         } catch (DocumentException e) {     
              e.printStackTrace();   
         }   
	}
	
	public void parseGraphServerConfig(Element element){
		if(element.getName().equals("GraphServerConfig")){
    		@SuppressWarnings("unchecked")
			List<Element> elements=element.elements();
    		for(Element ele:elements){
    			 parseGraphTypeNode(ele);
    		}
    	}
	}
	
	public void parseGraphTypeNode(Element element){
		if(element.getName().equals("GraphTypeNode")){
			String typeID = element.attribute("id").getText();
    		@SuppressWarnings("unchecked")
			List<Element> elements=element.elements();
    		for(Element ele:elements){
    			if(ele.getName().equals("GraphList")){
    				parseGraphNode(ele, typeID);
    			}else {
    				parseGraphTypeNode(ele);
    			}
    		}
    	}
	}
	
	public void parseGraphNode(Element element, String typeID){
		@SuppressWarnings("unchecked")
		List<Element> elements=element.elements();
		for(Element ele:elements){
			if(ele.getName().equals("GraphNode")){
				String active = ele.attribute("active").getText();
				if(active.equals("true")){
					GraphNode graph = new GraphNode();
					graph.setTypeID(typeID);
					graph.setId(ele.attribute("id").getText());
					graph.setName(ele.attribute("name").getText());
					graph.setActive(true);
					ArrayList<GraphSearchServerConfig> servers = new ArrayList<GraphSearchServerConfig>();
		    		@SuppressWarnings("unchecked")
					List<Element> eleServer=ele.elements();
		    		for(Element es:eleServer){
		    			GraphSearchServerConfig server = parseGraphServer(es);
		    			if(server!=null)
		    				servers.add(server);
		    		}
<<<<<<< HEAD
		    		graph.setSearchServers(servers);
		    		graphList.add(graph);
				}
	    	}
		}
	}
	
	public GraphSearchServerConfig parseGraphServer(Element element){
		GraphSearchServerConfig server = null;
		if(element.getName().equals("GraphSearchServerConfig")){
			String state = element.attribute("state").getText();
			if(state.equals("on")){
				GraphSearchServerConfig temp = new GraphSearchServerConfig();
				temp.setScheme(element.attribute("scheme").getText());
				temp.setHost(element.attribute("host").getText());
				temp.setEnterPath(element.attribute("enterPath").getText());
				temp.setEngineClass(element.attribute("engineClass").getText());
				temp.setState(true);
				server = temp;
			}
		}
		return server;	
	}
	
	public ArrayList<GraphNode> getGraphList() {
		return graphList;
	}

	public void setGraphList(ArrayList<GraphNode> graphList) {
		this.graphList = graphList;
	}

	public ArrayList<GraphTypeNode> getGraphTypeList() {
		return graphTypeList;
	}

	public void setGraphTypeList(ArrayList<GraphTypeNode> graphTypeList) {
		this.graphTypeList = graphTypeList;
	}

	public static void main (String args[]){
		XMLExtendReader reader = new XMLExtendReader();
		System.out.println(JSON.toJSONString(reader.getGraphList(), true));
		XMLReader reader1=new XMLReader();
		System.out.println(JSON.toJSONString(reader1.graphList,true));;
=======
		    		graph.setServers(servers);
		    		graphList.add(graph);
				}
	    	}
		}
	}
	
	public GraphSearchServerConfig parseGraphServer(Element element){
		GraphSearchServerConfig server = null;
		if(element.getName().equals("GraphSearchServerConfig")){
			String state = element.attribute("state").getText();
			if(state.equals("on")){
				GraphSearchServerConfig temp = new GraphSearchServerConfig();
				temp.setScheme(element.attribute("scheme").getText());
				temp.setHost(element.attribute("host").getText());
				temp.setEnterPath(element.attribute("enterPath").getText());
				temp.setEngineClass(element.attribute("engineClass").getText());
				temp.setState(true);
				server = temp;
			}
		}
		return server;
		
	}
	
	
	
	public ArrayList<GraphNode> getGraphList() {
		return graphList;
	}

	public void setGraphList(ArrayList<GraphNode> graphList) {
		this.graphList = graphList;
	}

	public ArrayList<GraphTypeNode> getGraphTypeList() {
		return graphTypeList;
	}

	public void setGraphTypeList(ArrayList<GraphTypeNode> graphTypeList) {
		this.graphTypeList = graphTypeList;
	}

	public static void main (String args[]){
		XMLExtendReader reader = new XMLExtendReader();
		System.out.println(JSON.toJSONString(reader.getGraphList(), true));
>>>>>>> refs/remotes/origin/master
	}
	
}
