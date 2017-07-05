package com.kgHub.pojo;

import java.util.Date;

public class ChildrenMissions {
    private Integer id;

    private Integer PId;

    private Integer state;

    private Date addTime;

    private Date finishTime;
    
    public Integer getId() {
        return id;
    }

    public void setId(Integer id) {
        this.id = id;
    }

    public Integer getPId() {
        return PId;
    }

    public void setPId(Integer PId) {
        this.PId = PId;
    }

    public Integer getState() {
        return state;
    }

    public void setState(Integer state) {
        this.state = state;
    }

    public Date getAddTime() {
        return addTime;
    }

    public void setAddTime(Date addTime) {
        this.addTime = addTime;
    }

    public Date getFinishTime() {
        return finishTime;
    }

    public void setFinishTime(Date finishTime) {
        this.finishTime = finishTime;
    }
    
    public void show(){
    	if(id!=null){
    		System.out.print("id:"+id);
    	}
    	if(PId!=null){
    		System.out.print(" PId:"+PId);
    	}
    	if(state!=null){
    		System.out.print(" state:"+state);
    	}
    	if(addTime!=null){
    		System.out.print(" addTime:"+addTime);
    	}
    	if(finishTime!=null){
    		System.out.print(" finishTime:"+finishTime);
    	}
    	System.out.print("\n");
    }
}