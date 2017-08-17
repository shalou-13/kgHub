package com.kgHub.service;

import java.util.ArrayList;

import com.kgHub.pojo.ChildrenMissions;

public interface IChildrenMissionService {
	
	public boolean insertChildMission(ChildrenMissions childrenMission); 
	
	public ArrayList<ChildrenMissions> GetAllChildMissions();

	public ChildrenMissions GetChildMissionById(int id);
	
	public boolean changeState(int id,int newstate);
}
