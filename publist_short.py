#!/usr/bin/env python

import ads
from ads_functions import *
import datetime
import time
from subprocess import call

# Change these three lines:
orcid='0000-0002-8466-7317'
name_strings=['Parker, M. L.','Parker, Michael L.', 'Parker, M.', 'Parker, Michael']
header_name="Michael Parker"

# Query ADS for orcid, retrieve all papers and associated info
query=ads.SearchQuery(orcid=orcid, rows=2000, \
                    fl=['id', 'bibcode', 'title', 'author', 'citation_count', 'year', 'page', 'volume', 'pub','pubdate'])
print("\nQuerying ADS for orcid:",orcid)
query.execute()

now=datetime.datetime.now()
print("Query executed",now.strftime("%Y-%m-%d %H:%M"),time.tzname[time.localtime().tm_isdst])

citations=[x.citation_count if x.citation_count is not None else 0 for x in query.articles]
years=[x.year for x in query.articles]
years_set=sorted(list(set(years)))[::-1]

print("Found",len(years),"records")
print("Total citations:",sum(citations))
print("h-index:",h_index(citations))

# Load the preamble and write to output .tex file
outfile=open('publication_list.tex','w')
preamble_file=open('preamble.tex')
for line in preamble_file:
    outfile.write(line)
preamble_file.close()


# Write intro lines to the publication list .tex file
outfile.write("\\makeheading{%s -- Publication List}" % header_name)
outfile.write("\\vspace{11pt}\\\\\nPublication list generated from ADS query for ORCID "+orcid)
outfile.write("\n\nQuery executed "+now.strftime("%Y-%m-%d %H:%M") + " " +\
            time.tzname[time.localtime().tm_isdst])
outfile.write("\n\n"+str(len(years))+" total records found, with "+str(sum(citations))+" total citations, h-index of "+str(h_index(citations))+".")
outfile.write("\n\nPublication list python script available from \\href{https://github.com/M-L-Parker/publist}{github.com/M-L-Parker/publist}\\\\\n")

#Filter papers by year:
papers=[]
first_author_papers=[]
for year in years_set:
    papers.append([])
    first_author_papers.append([])
for paper in query:
    i=years_set.index(paper.year)
    if "Parker" in paper.author[0]:
        first_author_papers[i].append(paper)
    else:
        papers[i].append(paper)


for i,year in enumerate(years_set):
    outfile.write("\n\\section{%s}" % str(year))

    # Write first-author papers to .tex file
    if len(first_author_papers[i])>0:
        outfile.write("\n\\textbf{Lead author:}")
        outfile.write("\n\\begin{itemize}\n\\setlength\\itemsep{-0.5em}")
        for paper in first_author_papers[i]:
            if "#" not in paper.pub and "X-ray Universe" not in paper.pub and "Garden" not in paper.pub: # Filter some crap.
                # Some conference proceedings can find their way in, and I can't think of a smart way of doing this.
                # This set of filters is unlikely to have much effect for other people.

                author_str=shorten_authors(paper.author,name_strings) # should return author list string

                outfile.write("\n\n\\item \\emph{"+paper.title[0]+"}\\\\")
                outfile.write("\n"+author_str+"\\\\")
                if paper.volume is not None:
                    outfile.write("\n"+paper.pub+", "+paper.volume+", "+paper.page[0]+"\\\\")
                else:
                    if paper.page is not None:
                        outfile.write("\n"+paper.pub+", "+paper.page[0]+"\\\\")
                    else:
                        outfile.write("\n"+paper.pub+"\\\\")
                if paper.citation_count is not None and paper.citation_count != 0:
                    outfile.write("\nCited by "+str(paper.citation_count)+"\\\\")

        outfile.write("\n\\end{itemize}")

    # Write co-author papers to .tex file
    if len(papers[i])>0:
        outfile.write("\n\\textbf{Co-author:}")
        outfile.write("\n\\begin{itemize}\n\\setlength\\itemsep{-0.50em}")
        for paper in papers[i]:
            if "#" not in paper.pub and "X-ray Universe" not in paper.pub: # Filter some crap.
                # Some conference proceedings can find their way in, and I can't think of a smart way of doing this.
                # This set of filters is unlikely to have much effect for other people.

                author_str=shorten_authors(paper.author,name_strings) # should return author list string
                outfile.write("\n\n\\item \\emph{"+paper.title[0]+"}\\\\")
                outfile.write("\n"+author_str+"\\\\")
                if paper.volume is not None:
                    outfile.write("\n"+paper.pub+", "+paper.volume+", "+paper.page[0]+"\\\\")
                else:
                    if paper.page is not None:
                        outfile.write("\n"+paper.pub+", "+paper.page[0]+"\\\\")
                if paper.citation_count is not None and paper.citation_count != 0:
                    outfile.write("\nCited by "+str(paper.citation_count)+"\\\\")

        outfile.write("\n\\end{itemize}")

outfile.write("\n\\end{document}")
outfile.close()

print("Calling xelatex")
call(["xelatex publication_list.tex >> pdflatex.log"],shell=True)
