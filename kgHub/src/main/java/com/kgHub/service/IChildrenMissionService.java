package com.kgHub.service;

import com.kgHub.pojo.ChildrenMissions;
import com.kgHub.pojo.ChildrenMissionsWithBLOBs;

public interface IChildrenMissionService {
	
	public boolean insertChildMission(ChildrenMissionsWithBLOBs childrenMission); 
	
	public ChildrenMissions GetChildMissionById(int id);
	
	public boolean changeState(int id,int newstate);
}
