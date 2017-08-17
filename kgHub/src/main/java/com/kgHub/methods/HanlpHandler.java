package com.kgHub.methods;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import com.hankcs.hanlp.HanLP;
import com.hankcs.hanlp.seg.Segment;
import com.hankcs.hanlp.seg.common.Term;
import com.hankcs.hanlp.tokenizer.BasicTokenizer;


public class HanlpHandler {
	
	public static Map<String,List<String>> nlp(String text){
		Segment segment=HanLP.newSegment().enableCustomDictionary(true);
		java.util.List<Term> list=segment.seg(text);
		Map<String, List<String>> map=new HashMap<>();
		ArrayList<String> verblist=new ArrayList<>();
		ArrayList<String> nounlist=new ArrayList<>();
		ArrayList<String> adlist=new ArrayList<>();
		for(Term term:list){
			switch (term.nature.toString().charAt(0)){
			case 'a':
				adlist.add(term.word);
				break;
			case 'd':
				adlist.add(term.word);
				break;
			case 'n':
				nounlist.add(term.word);
				break;
			case 'v':
				verblist.add(term.word);
				break;
			default:
				break;
			}
		}
		map.put("v",verblist);
		map.put("n",nounlist);
		map.put("ad",adlist);
		return map;
	}
	
	public static Map<String,Map<String,String>> nlpspecific(String text){
		Segment segment=HanLP.newSegment();
		java.util.List<Term> list=segment.seg(text);
		Map<String,Map<String,String>> map=new HashMap<>();
		Map<String,String> verbmap=new HashMap<>();
		Map<String,String> nounmap=new HashMap<>();
		Map<String,String> admap=new HashMap<>();
		for(Term term:list){
			switch (term.nature.toString().charAt(0)){
			case 'a':
				admap.put(term.word,term.nature.toString());
				break;
			case 'd':
				admap.put(term.word,term.nature.toString());
				break;
			case 'n':
				nounmap.put(term.word,term.nature.toString());
				break;
			case 'v':
				verbmap.put(term.word,term.nature.toString());
				break;
			default:
				break;
			}
		}
		map.put("v",verbmap);
		map.put("n",nounmap);
		map.put("ad",admap);
		return map;
	}
	
	public static Map<String,List<String>> nlpWithLearning(String text){
		Map<String,List<String>> map=new HashMap<>();
		return map;
	}
	
	public static void main(String[] args){
		Map<String,Map<String,String>> map=HanlpHandler.nlpspecific("八宝山殡仪馆的面积？");
		System.out.println(map);
		System.out.println(BasicTokenizer.segment("八宝山殡仪馆怎么走？"));
		System.out.println(BasicTokenizer.segment("八宝山殡仪馆的面积？"));
		System.out.println(BasicTokenizer.segment("张三的火化时间？"));
	}
}
