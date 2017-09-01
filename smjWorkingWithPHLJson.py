import urllib2
 
proxy = urllib2.ProxyHandler({'http': '172.26.67.10:8080'})
opener = urllib2.build_opener(proxy)
urllib2.install_opener(opener)

print urllib2.getproxies()

print urllib2.urlopen('http://www.google.com')

#response = urllib2.urlopen('http://www.google.com')
#datum = response.read().decode("UTF-8")
#response.close()
#print datum
