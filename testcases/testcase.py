#!/usr/bin/python
# -*-coding:utf-8-*-

import os,sys
import unittest
from os.path import expanduser
sys.path.append('../')
from wcs.commons.config import Config
from wcs.services.client import Client
from wcs.commons.putpolicy import PutPolicy
from wcs.commons.logme import debug
from wcs.commons.util import urlsafe_base64_encode
print (sys.version)
config_file = os.path.join(expanduser("~"), ".wcscfg")

class WcsTestCases(unittest.TestCase):

    def setUp(self):
        self.cfg = Config(config_file)
        self.cli = Client(self.cfg)
        self.bucket = 'qz-mulitupload-caiyz-test'
        self.filepath = 'E:\\157.jpg'
    #文件直传
    def test_simple_upload(self):
        key = '20180408.jpg'
        path = self.filepath
        return_data = self.cli.simple_upload(path, self.bucket, key)
        debug(return_data)
        self.assertEqual(return_data[0],200)

    #流数据上传
    def test_stream_upload(self):
        stream = 'http://big-caiyz-fmgr-cache.com/1m.jpg'
        key = '1m.jpg'
        return_data = self.cli.stream_upload(stream, self.bucket, key)
        debug(return_data)
        self.assertEqual(return_data[0],200)

    #分片上传（有同名文件直接覆盖）
    def test_multipart_upload(self):
        path = 'F:\\5_.zip'
        key = '5_.zip'
        self.cfg.overwrite = 1
        return_data = self.cli.multipart_upload(path, self.bucket, key)
        debug(return_data)
        self.assertEqual(return_data[0],200)
        
    #智能上传（文件大于10M启用分片上传，有同名文件直接覆盖）
    def test_samrt_upload(self):
        path = '/root/caiyz/data/14M'
        key = '100-2M'
        self.cfg.overwrite =1
        debug(self.cli.smart_upload(path, self.bucket, key, 10))

    #列举空间
    def test_bucket_list(self):
        return_data = self.cli.bucket_list('list-bucket')
        debug(return_data)
        self.assertEqual(return_data[0],200)

    # 指定mode=0，指定prefix精确匹配，获取空间文件
    def test_list_mode_0_prefix_exact(self):
        #print u'用例开始：\n'
        self.bucket_list = 'list-bucket'
        return_data = self.cli.bucket_list(self.bucket_list,mode='',prefix='temp_1')
        print ("返回结果:{0}".format(return_data))
        self.assertEqual(return_data[0],200)
        #生成的结果与预期结果对比


    #空间状态信息
    def test_bucket_stat(self):
        startdate = '2017-11-10'
        enddate = '2017-11-12'
        return_data = self.cli.bucket_stat(self.bucket, startdate, enddate)
        debug(return_data)
        self.assertEqual(return_data[0],200)

    #文件信息查询
    def test_stat(self):
        key = '5_.zip'
        return_data = self.cli.stat(self.bucket, key)
        debug(return_data)
        self.assertEqual(return_data[0],200)

    #文件删除
    def test_delete(self):
        key ='5_.zip'
        return_data = self.cli.delete(self.bucket,key)
        debug(return_data)
        self.assertEqual(return_data[0],200)

    #文件移动
    def test_move(self):
        path = 'F:\\5_.zip'
        key = '5_.zip'
        self.cfg.overwrite = 1
        self.cli.multipart_upload(path, self.bucket, key)
        srckey = '5_.zip'
        dstkey = '5_1.zip'
        return_data = self.cli.move(self.bucket, srckey, self.bucket)
        debug(return_data)
        self.assertEqual(return_data[0],200)

    #文件复制
    def test_copy(self):
        path = 'F:\\5_.zip'
        key = '5_.zip'
        self.cfg.overwrite = 1
        self.cli.multipart_upload(path, self.bucket, key)
        srckey = '5_.zip'
        dstkey = '5_2.zip'
        return_data = self.cli.copy(self.bucket, srckey, self.bucket,dstkey)
        debug(return_data)
        self.assertEqual(return_data[0],200)

    #文件过期时间设置
    def test_setdeadline(self):
        path = 'F:\\5_.zip'
        key = '5_.zip'
        self.cfg.overwrite = 1
        self.cli.multipart_upload(path, self.bucket, key)
        deadline = '1'
        return_data = self.cli.setdeadline(self.bucket, key, deadline)
        debug(return_data)
        self.assertEqual(return_data[0],200)

    #fmgr 文件移动
    def test_fmgr_move(self):
        path = 'F:\\5_.zip'
        key = '5_.zip'
        self.cfg.overwrite = 1
        self.cli.multipart_upload(path, self.bucket, key)
        srckey = key
        dstkey =  '5_3.zip'
        resource = urlsafe_base64_encode('%s:%s' % (self.bucket,srckey))
        fops = 'resource/%s/bucket/%s/key/%s' % (resource,urlsafe_base64_encode(self.bucket), urlsafe_base64_encode(dstkey))
        return_data = self.cli.fmgr_move(fops)
        debug(return_data)
        self.assertEqual(return_data[0],200)

    #fmgr 文件复制
    def test_fmgr_copy(self):
        path = 'F:\\5_.zip'
        key = '5_.zip'
        self.cfg.overwrite = 1
        self.cli.multipart_upload(path, self.bucket, key)
        srckey = key
        dstkey = '5_4.zip'
        resource = urlsafe_base64_encode('%s:%s' % (self.bucket,srckey))
        fops = 'resource/%s/bucket/%s/key/%s' % (resource,urlsafe_base64_encode(self.bucket), urlsafe_base64_encode(dstkey))
        return_data = self.cli.fmgr_copy(fops)
        debug(return_data)
        self.assertEqual(return_data[0],200)

    #fmgr 文件fetch
    def test_fmgr_fetch(self):
        url = 'http://big-caiyz-fmgr-cache.com/1m.jpg'
        key = 'fetch_1m.jpg'
        fetchurl = urlsafe_base64_encode(url)
        enbucket = urlsafe_base64_encode(self.bucket)
        enkey = urlsafe_base64_encode(key)
        fops = 'fetchURL/%s/bucket/%s/key/%s' % (fetchurl, enbucket, enkey)
        return_data = self.cli.fmgr_fetch(fops)
        debug(return_data)
        self.assertEqual(return_data[0],200)

    #fmgr 文件删除
    def test_fmgr_delete(self):
        path = 'F:\\5_.zip'
        key = '5_.zip'
        self.cfg.overwrite = 1
        self.cli.multipart_upload(path, self.bucket, key)
        enbucket = urlsafe_base64_encode(self.bucket)
        enkey = urlsafe_base64_encode(key)
        fops = 'bucket/%s/key/%s' % (enbucket, enkey)
        return_data = self.cli.fmgr_delete(fops)
        debug(return_data)
        self.assertEqual(return_data[0],200)

    #fmgr 按前缀删除文件
    def test_fmgr_prefix_del(self):
        path = 'F:\\5_.zip'
        key = 'aa/5_.zip'
        self.cfg.overwrite = 1
        self.cli.multipart_upload(path, self.bucket, key)
        prefix = 'aa'
        enbucket = urlsafe_base64_encode(self.bucket)
        enprefix = urlsafe_base64_encode(prefix)
        fops = 'bucket/%s/prefix/%s' % (enbucket, enprefix)
        return_data = self.cli.prefix_delete(fops)
        debug(return_data)
        self.assertEqual(return_data[0],200)

    #fmgr m3u8文件删除
    def test_fmgr_m3u8_del(self):
        self.cfg.overwrite = 1
        key = 'M3U8_FILE.m3u8'
        key_ts = '000001.ts'
        path = 'E:\\m3u8\\M3U8_FILE.m3u8'
        path_ts = 'E:\\m3u8\\000001.ts'
        debug('start to upload m3u8')
        self.cli.simple_upload(path, self.bucket, key)
        debug('start to upload ts file')
        self.cli.simple_upload(path_ts, self.bucket, key_ts)
        enbucket = urlsafe_base64_encode(self.bucket)
        enkey = urlsafe_base64_encode(key)
        fops = 'bucket/%s/key/%s' % (enbucket, enkey)
        return_data = self.cli.m3u8_delete(fops)
        debug(return_data)
        self.assertEqual(return_data[0],200)

    #fmgr 任务状态查询
    def test_fmgr_stat(self):
        path = 'F:\\5_.zip'
        key = '5_.zip'
        self.cfg.overwrite = 1
        self.cli.multipart_upload(path, self.bucket, key)
        enbucket = urlsafe_base64_encode(self.bucket)
        enkey = urlsafe_base64_encode(key)
        fops = 'bucket/%s/key/%s' % (enbucket, enkey)
        return_data = self.cli.fmgr_delete(fops)
        debug(return_data)
        persistentId = return_data[1].get('persistentId')
        return_data = self.cli.fmgr_status(persistentId)
        debug(return_data)
        self.assertEqual(return_data[0],200)

    #音视频持久化操作
    def test_ops(self):
        self.cfg.overwrite = 1
        key = 'huhu.mp4'
        path = 'E:\\huhu.mp4'
        debug('start to upload huhu.mp4')
        self.cli.simple_upload(path, self.bucket, key)
        fops = 'vframe/jpg/offset/10|saveas/cXotbXVsaXR1cGxvYWQtY2FpeXotdGVzdDrop4bpopHmiKrlm74uanBn'
        return_data = self.cli.ops_execute(fops,self.bucket,key)
        debug(return_data)
        self.assertEqual(return_data[0],200)

    #音视频处理结果查询
    def test_ops_status(self):
        self.cfg.overwrite = 1
        key = 'huhu.mp4'
        path = 'E:\\huhu.mp4'
        debug('start to upload huhu.mp4')
        self.cli.simple_upload(path, self.bucket, key)
        fops = 'vframe/jpg/offset/10|saveas/cXotbXVsaXR1cGxvYWQtY2FpeXotdGVzdDrop4bpopHmiKrlm74uanBn'
        return_data = self.cli.ops_execute(fops,self.bucket,key)
        persistentId = return_data[1].get('persistentId')
        return_data = self.cli.ops_status(persistentId)
        debug(return_data)
        self.assertEqual(return_data[0],200)

    def test_wslive_list(self):
        channel = ''
        startTime = ''
        endTime = ''
        debug(self.cli.wslive_list(channel, startTime, endTime,self.bucket))

    #查询统计数据
    def test_bucket_statistics(self):
        return_data = self.cli.bucket_statistics(self.bucket, 'uploadRequest', '2019-12-20', '2019-12-31')
        debug(return_data)
        self.assertEqual(return_data[0],200)

    def test_image_detect(self):
        return_data = self.cli.image_detect('http://wcsd.chinanetcenter.com/xdd_15779502234034.png', 'porn', 'doc-pics')
        debug(return_data)
        self.assertEqual(return_data[0],200)

if __name__ == '__main__':
    suite = unittest.TestSuite()
    suite.addTest(WcsTestCases("test_image_detect"))
    runner = unittest.TextTestRunner()
    runner.run(suite)
