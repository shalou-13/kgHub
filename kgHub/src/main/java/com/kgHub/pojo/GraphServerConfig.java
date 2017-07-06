package com.kgHub.pojo;

public class GraphServerConfig {
	public String type;
	public String URL;
	public String userName;
	public String password;
	public boolean state;
	
	public String getType(){
		return this.type;
	}
	
	public String getURL(){
		return this.URL;
	}
	
	public String getUserName(){
		return this.userName;
	}
	
	public String getPassword(){
		return this.password;
	}
	
	public boolean getState(){
		return this.state;
	}
	
	public void setType(String type){
		this.type=type;
	}
	
	public void setURL(String URL){
		this.URL=URL;
	}
	
	public void setUserName(String userName){
		this.userName=userName;
	}
	
	public void setPassword(String password){
		this.password=password;
	}
	
	public void setState(boolean state){
		this.state=state;
	}
}
