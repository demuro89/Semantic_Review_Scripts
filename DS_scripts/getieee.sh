
# pdf normali
#cat ../links_old.txt | grep "\.pdf" | while read paper; do name=`echo $paper | awk -F "/" "{ print $NF }"`; echo "Downlading paper : $name"; wget $paper
#done
#/di

# ieee explore
cat ../da_sorgenti/ieee_link.txt |  while read paper; do echo "Downlading paper : $paper"; 

curl "$paper" -H "User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.1.1 Safari/605.1.15" -H "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8" -H "Accept-Language: en-US,en;q=0.5" --compressed -H "Connection: keep-alive" -H "Cookie: utag_main=v_id:0165827f1f9a001e220f4cd333100104400360090086e$_sn:3$_ss:0$_st:1562166163998$vapi_domain:ieee.org$ses_id:1562164361011%3Bexp-session$_pn:1%3Bexp-session; fp=f1981fb577cefdc4af87ae03f5c67eab; AMCV_8E929CC25A1FB2B30A495C97%40AdobeOrg=1687686476%7CMCIDTS%7C17772%7CMCMID%7C78066098789675820813784191430146940824%7CMCAAMLH-1562769162%7C6%7CMCAAMB-1562769162%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1562171562s%7CNONE%7CMCAID%7CNONE%7CvVersion%7C3.0.0" -H "Upgrade-Insecure-Requests: 1" --output ../ieee/$paper.pdf
sleep 2
done

# arxiv con script python

# springer cambiare url da 

# acm prendere il link