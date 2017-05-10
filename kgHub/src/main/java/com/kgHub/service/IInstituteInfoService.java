package com.kgHub.service;

import java.util.ArrayList;

import com.kgHub.pojo.InstituteInfo;

public interface IInstituteInfoService {
	
	public InstituteInfo getInstituteInfoById(String instituteId);
	
	public ArrayList<InstituteInfo> getAllInstituteInfos();
}
