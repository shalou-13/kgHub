package com.kgHub.pojo;

import java.util.ArrayList;

<<<<<<< HEAD
import com.mysql.fabric.xmlrpc.base.Array;

public class GraphNode {
	
	public String id;
	public String name;
	public boolean active;
	public String typeID;
	public ArrayList<GraphServerConfig> servers;
	public ArrayList<GraphSearchServerConfig> searchServers;
	
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
	public ArrayList<GraphSearchServerConfig> getSearchServers() {
		return searchServers;
	}
	public void setSearchServers(ArrayList<GraphSearchServerConfig> servers) {
		this.searchServers = servers;
	}
	
	public ArrayList<GraphServerConfig> getServers() {
		return servers;
	}
	
	public void setServers(ArrayList<GraphServerConfig> servers){
		this.servers=servers;
	}
	
=======
public class GraphNode {
	
	public String id;
	public String name;
	public boolean active;
	public String typeID;
	public ArrayList<GraphSearchServerConfig> servers;
	
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
	public ArrayList<GraphSearchServerConfig> getServers() {
		return servers;
	}
	public void setServers(ArrayList<GraphSearchServerConfig> servers) {
		this.servers = servers;
	}
>>>>>>> refs/remotes/origin/master
	public String getTypeID() {
		return typeID;
	}
	public void setTypeID(String typeID) {
		this.typeID = typeID;
	}
	
	
	
	

}
