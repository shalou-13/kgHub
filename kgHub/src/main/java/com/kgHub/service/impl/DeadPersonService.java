package com.kgHub.service.impl;

import java.util.ArrayList;

import javax.annotation.Resource;

import org.springframework.stereotype.Service;

import com.kgHub.dao.DeadPersonMapper;
import com.kgHub.pojo.DeadPerson;
import com.kgHub.service.IDeadPersonService;

@Service("deadPersonService")
public class DeadPersonService implements IDeadPersonService {
	
	@Resource
	private DeadPersonMapper deadPersonDao;

	@Override
	public ArrayList<DeadPerson> getAllDeadPersons() {
		return (ArrayList<DeadPerson>)this.deadPersonDao.selectAllDeadPersons();
	}

}
