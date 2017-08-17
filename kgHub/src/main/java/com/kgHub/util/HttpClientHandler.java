package com.kgHub.util;

import java.io.IOException;
import java.io.UnsupportedEncodingException;
import java.net.URI;
import java.net.URISyntaxException;

import org.apache.http.HttpEntity;
import org.apache.http.HttpStatus;
import org.apache.http.client.ClientProtocolException;
import org.apache.http.client.methods.CloseableHttpResponse;
import org.apache.http.client.methods.HttpPost;
import org.apache.http.client.utils.URIBuilder;
import org.apache.http.entity.StringEntity;
import org.apache.http.impl.client.CloseableHttpClient;
import org.apache.http.impl.client.HttpClients;
import org.apache.http.util.EntityUtils;
import org.apache.log4j.Logger;

import com.alibaba.fastjson.JSON;
import com.alibaba.fastjson.JSONObject;




public class HttpClientHandler {
	
	private static Logger logger = Logger.getLogger(JsonHandler.class);
	
	
	/**
	 * the http post method
	 * @param apiServer  search server url
	 * @param json  the post parameters of JSON type.
	 * @param reqPath the request relative path, such as "/search".
	 * @return the JSON String type result.
	 */
	
	public static String doPost(String path, String host, String scheme, String json){
			CloseableHttpClient httpclient = HttpClients.createDefault();
			String result = null;
			try {
				URI uri = generateUri(path, host, scheme);
				HttpPost post = new HttpPost(uri);
				StringEntity s = new StringEntity(json.toString(), "utf-8");
				s.setContentEncoding("UTF-8");
				s.setContentType("application/json");// 发送json数据需要设置contentType
				post.setEntity(s);
				CloseableHttpResponse response = httpclient.execute(post);
				try{
					HttpEntity entity = response.getEntity();
					if (response.getStatusLine().getStatusCode() == HttpStatus.SC_OK) {
						result = EntityUtils.toString(entity, "utf-8");
					}
					EntityUtils.consume(entity);
				}finally{
					response.close();
				}
			}catch (ClientProtocolException e) {  
	            e.printStackTrace();  
	            logger.error(e.toString());
	        } catch (UnsupportedEncodingException e) {  
	            e.printStackTrace();  
	            logger.error(e.toString());
	        } catch (IOException e) {  
	            e.printStackTrace();  
	            logger.error(e.toString());
	        } catch (URISyntaxException e) {
				e.printStackTrace();
				logger.error(e.toString());
			}finally {
				try {
					httpclient.close();
				} catch (IOException e) {
					e.printStackTrace();
					logger.error(e.toString());
				}
			}
			if(result == null){
				JSONObject jsonObject = JSONObject.parseObject(JSON.toJSONString(JsonHandler.writeJsontoResponse(3001, ""))); 
				result = jsonObject.toString();
			}
			return result;
		}
	
	/**
	 * generate URI by apiServer and request path.
	 * @param apiServer the type of apiServer ,include onlineSacrifice, technology, culture, u3d, recommend servers.
	 * @param path the request relative path, such as "/search".
	 * @return the URI Object.
	 * @throws URISyntaxException
	 */
	public static URI generateUri(String path, String host, String scheme) throws URISyntaxException{
		URI uri = null;
		uri = new URIBuilder().setScheme(scheme)
				.setHost(host)
				.setPath(path)
				.build();
		return uri;
	}
	
}
