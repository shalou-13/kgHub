package com.kgHub.service.impl;

import java.util.ArrayList;

import javax.annotation.Resource;

import org.springframework.stereotype.Service;

import com.kgHub.dao.InstituteInfoMapper;
import com.kgHub.pojo.InstituteInfo;
import com.kgHub.service.IInstituteInfoService;

@Service("instituteInfoService")
public class InstituteInfoService implements IInstituteInfoService {
	
	@Resource
	private InstituteInfoMapper instituteInfoDao;

	@Override
	public InstituteInfo getInstituteInfoById(String instituteId) {
		return this.instituteInfoDao.selectByPrimaryKey(instituteId);
	}

	@Override
	public ArrayList<InstituteInfo> getAllInstituteInfos() {
		return (ArrayList<InstituteInfo>)this.instituteInfoDao.selectAllInstituteInfos();
	}
	
	

}
