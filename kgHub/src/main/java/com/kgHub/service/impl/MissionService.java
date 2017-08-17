package com.kgHub.service.impl;

import java.util.ArrayList;

import javax.annotation.Resource;

import org.springframework.stereotype.Service;

import com.kgHub.dao.MissionsMapper;
import com.kgHub.pojo.MissionsWithBLOBs;
import com.kgHub.service.IMissionService;

@Service
public class MissionService implements IMissionService{

	private final static int keywordnum=4;
	private final static int rkeynum=0;
	private final static int nkeynum=1;
	private final static int vkeynum=2;
	private final static int akeynum=3;
	
	@Resource
	private MissionsMapper missionMapperDao;
	

	@Override
	public boolean changeStateById(int id, int state) {
		// TODO Auto-generated method stub
		MissionsWithBLOBs mission=new MissionsWithBLOBs();
		mission.setState(state);
		mission.setId(id);
		try {
			missionMapperDao.updateByPrimaryKeySelective(mission);
		}catch(Exception e) {
			// TODO: handle exception
			return false;
		}
		return true;
	}

	@Override
	public ArrayList<MissionsWithBLOBs> getAllMissions() {
		// TODO Auto-generated method stub
		return (ArrayList<MissionsWithBLOBs>)missionMapperDao.selectAllMissions();
	}

	@Override
	public MissionsWithBLOBs getMissionById(int id) {
		// TODO Auto-generated method stub
		return (MissionsWithBLOBs)missionMapperDao.selectByPrimaryKey(id);
	}

	@Override
	public String[] getKeywordsById(int id) {
		// TODO Auto-generated method stub
		String[] keywords=new String[keywordnum];
		MissionsWithBLOBs mission=(MissionsWithBLOBs)missionMapperDao.selectByPrimaryKey(id);
		keywords[rkeynum]=mission.getRkeyword();
		keywords[nkeynum]=mission.getNkeyword();
		keywords[vkeynum]=mission.getVkeyword();
		keywords[akeynum]=mission.getAkeyword();
		return null;
	}

	@Override
	public boolean insertMission(MissionsWithBLOBs missionsWithBLOBs) {
		// TODO Auto-generated method stub
		/*MissionsWithBLOBs missionsWithBLOBs=new MissionsWithBLOBs();
		missionsWithBLOBs.setRkeyword(Rkeyword);
		missionsWithBLOBs.setNkeyword(Nkeyword);
		missionsWithBLOBs.setVkeyword(Vkeyword);
		missionsWithBLOBs.setAkeyword(Akeyword);
		missionsWithBLOBs.setState(state);*/
		try {
			missionMapperDao.insertSelective(missionsWithBLOBs);
		} catch (Exception e) {
			// TODO: handle exception
			e.printStackTrace();
			return false;
		}
		return true;
	}

}
