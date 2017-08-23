package com.kgHub.methods;

import java.util.ArrayList;
import java.util.HashMap;

import javax.annotation.Resource;

import org.springframework.stereotype.Service;

import com.alibaba.fastjson.JSONObject;
import com.kgHub.pojo.ChildrenMissionsWithBLOBs;
import com.kgHub.pojo.GraphNode;
import com.kgHub.pojo.UserPortrait;
import com.kgHub.service.impl.ChildrenMissionService;
import com.kgHub.service.impl.UserPortraitService;

@Service
public class UserPortraitHandler {
	
	@Resource
	private ChildrenMissionService childrenMissionService;
	@Resource
	private UserPortraitService userPortraitService;

	public void computeUserPortrait(int userID){
		XMLExtendReader reader = new XMLExtendReader();
		ArrayList<GraphNode> graphList = reader.getGraphList();
		HashMap<String, Object> portrait = new HashMap<String, Object>();
		for(GraphNode graph: graphList){
			ArrayList<ChildrenMissionsWithBLOBs> result = childrenMissionService.selectChildMissionsByUserID(userID, graph.getId());
			double weight = 0;
			for(ChildrenMissionsWithBLOBs cm : result){
				if(cm.getResult()!=null && !cm.getResult().equals("")){
					JSONObject obj = JSONObject.parseObject(cm.getResult());
					weight = weight + (obj.containsKey("weight")==true?obj.getDouble("weight"):0);
				}
			}
			weight = weight/result.size();
			portrait.put(graph.getId(), weight);
		}
		UserPortrait up = userPortraitService.selectByUserID(2);
		if(up!=null){
			up.setPortrait(JSONObject.toJSONString(portrait));
			userPortraitService.updateUserPortraitSelective(up);
		}else{
			up = new UserPortrait();
			up.setUserID(userID);
			up.setPortrait(JSONObject.toJSONString(portrait));
			userPortraitService.insertSelective(up);
		}
		
	}
}
