package com.kgHub.service;

import java.util.ArrayList;

import com.kgHub.pojo.MissionsWithBLOBs;

public interface IMissionService {
	
	public boolean insertMission(MissionsWithBLOBs missionsWithBLOBs);
	
	public boolean changeStateById(int state, int id);
	
	public ArrayList<MissionsWithBLOBs> getAllMissions();
	
	public MissionsWithBLOBs getMissionById(int id);
	
	public String[] getKeywordsById(int id);
}
