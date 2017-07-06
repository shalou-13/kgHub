package com.kgHub.pojo;

import java.util.ArrayList;

public class GraphTypeNode {

	public String id;
	public String name;
	public boolean active;
	public ArrayList<GraphNode> graphList;
	
	public String getId() {
		return id;
	}
	public void setId(String id) {
		this.id = id;
	}
	public String getName() {
		return name;
	}
	public void setName(String name) {
		this.name = name;
	}
	public boolean isActive() {
		return active;
	}
	public void setActive(boolean active) {
		this.active = active;
	}
	public ArrayList<GraphNode> getGraphList() {
		return graphList;
	}
	public void setGraphList(ArrayList<GraphNode> graphList) {
		this.graphList = graphList;
	}
	
	
}
