package com.kgHub.service.impl;

import java.util.ArrayList;

import javax.annotation.Resource;

import org.springframework.stereotype.Service;

import com.kgHub.dao.ChildrenMissionsMapper;
import com.kgHub.pojo.ChildrenMissions;
import com.kgHub.service.IChildrenMissionService;

@Service
public class ChildrenMissionService implements IChildrenMissionService{
	
	@Resource
	private ChildrenMissionsMapper childrenMissionsDao;

	@Override
	public ArrayList<ChildrenMissions> GetAllChildMissions() {
		// TODO Auto-generated method stub
		return (ArrayList<ChildrenMissions>)(this.childrenMissionsDao.selectAllChildrenMissions());
	}

	@Override
	public ChildrenMissions GetChildMissionById(int id) {
		// TODO Auto-generated method stub
		return (ChildrenMissions)(this.childrenMissionsDao.selectByPrimaryKey(id));
	}

	@Override
	public boolean changeState(int id,int newstate) {
		// TODO Auto-generated method stub
		ChildrenMissions childrenMission=new ChildrenMissions();
		childrenMission.setState(newstate);
		childrenMission.setId(id);
		try{
			this.childrenMissionsDao.updateByPrimaryKeySelective(childrenMission);
		}
		catch (Exception e) {
			// TODO: handle exception
			e.printStackTrace();
			return false;
		}
		return true;
	}

	@Override
	public boolean insertChildMission(ChildrenMissions childrenMission) {
		// TODO Auto-generated method stub
		/*ChildrenMissions childrenMission=new ChildrenMissions();
		childrenMission.setState(state);
		childrenMission.setPId(PId);*/
		try{
			this.childrenMissionsDao.insertSelective(childrenMission);
		}
		catch (Exception e) {
			// TODO: handle exception
			e.printStackTrace();
			return false;
		}
		return true;
	}
	
}
