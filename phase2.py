import os

def main():
    os.system("sort -u -o recsSorted.txt recs.txt")
    os.system("sort -u -o emailsSorted.txt emails.txt")
    os.system("sort -u -o datesSorted.txt dates.txt")
    os.system("sort -u -o termsSorted.txt terms.txt")

    os.system("perl break.pl < recsSorted.txt > recsTemp.txt")
    os.system("perl break.pl < emailsSorted.txt > emailsTemp.txt")
    os.system("perl break.pl < datesSorted.txt > datesTemp.txt")
    os.system("perl break.pl < termsSorted.txt > termsTemp.txt")
 
    os.system("db_load -c duplicates=0 -T -t hash -f recsTemp.txt re.idx")
    os.system("db_load -c duplicates=1 -T -t btree -f termsTemp.txt te.idx")
    os.system("db_load -c duplicates=1 -T -t btree -f emailsTemp.txt em.idx")
    os.system("db_load -c duplicates=1 -T -t btree -f datesTemp.txt da.idx")
   


main()
