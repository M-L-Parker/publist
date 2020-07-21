import numpy as np
from datetime import datetime
from matplotlib import pyplot as pl
from pylatexenc.latexencode import utf8tolatex

def boldname(string,name_strings):
    """Adds \\textbf{} around any names given in name_strings (should be a list).
    Note that names with initials included should come before names without.
    I could fix this, but can't be bothered."""
    for name in name_strings:
        if name in string:
            string=string.replace(name, "\\textbf{%s}" % name)
            return string

def shorten_authors(authors,name_strings,threshold=3):
    """Shorten the author list, adding et al., ... etc."""
    # authors=string.split("; ")
    length=len(authors)
    if length<=threshold:
        author_str=boldname(special_characters("; ".join(authors)),name_strings)
        # return
    else:
        if authors[0] in name_strings:
            short_authors=authors[0]

            author_str= boldname(special_characters("; ".join(authors[:threshold])),name_strings)+"; et al."
        else:
            if authors[-1] in name_strings:
                author_str=author_str=special_characters("; ".join(authors[:threshold]))+"; ... \\textbf{"+authors[-1]+"}"
            else:
                for i,author in enumerate(authors):
                    if author in name_strings:
                        highlight_author=author
                        final_index=i
                if final_index==threshold:
                    author_str=special_characters("; ".join(authors[:threshold]))+"; \\textbf{"+highlight_author+"}; et al."
                else:
                    if final_index>threshold:
                        author_str=special_characters("; ".join(authors[:threshold]))+"; ... \\textbf{"+highlight_author+"}; et al."
                    else:
                        author_str=boldname(special_characters("; ".join(authors[:threshold])),name_strings)+"; et al."
    print(author_str)
    return author_str

def special_characters(string):
    """read a string from ADS, usually author names, and replace special characters with the correct latex"""
    string=utf8tolatex(string)
    return string

def step_plot(xdata,ydata,xerrors,axis=None,**kwargs):
    new_x=[]
    new_y=[]
#     new_x.append(xdata[0]-xerrors[0])
#     new_y.append(ydata[0])
    for i in range(0,len(xdata)):
        new_x.append(xdata[i]-xerrors[i])
        new_x.append(xdata[i]+xerrors[i])
        new_y.append(ydata[i])
        new_y.append(ydata[i])
#     new_x.append(xdata[-1]+xerrors[-1])
#     new_y.append(ydata[-1])
    if axis==None:
        pl.plot(new_x,new_y,**kwargs)
    else:
        axis.plot(new_x,new_y,**kwargs)

def h_index(citations):
    sorted_citations = sorted(citations)[::-1]
    for i, c in enumerate(sorted_citations):
        if i >= c:
            return i
    return len(citations)


def get_citations_of_papers(metrics):
    """
    Convert the metrics into a format that is easier to work with. Year-ordered
    numpy arrays.
    """
    year_citation, ref_to_ref, ref_to_non_ref, non_ref_to_ref, non_ref_to_non_ref = \
        [], [], [], [], []

    citations = metrics['histograms']['citations']

    y = list(citations['refereed to refereed'].keys())
    y.sort()
    for i in range(len(y)):
        k = y[i]
        year_citation.append(datetime.strptime(k, '%Y'))
        ref_to_ref.append(citations['refereed to refereed'][k])
        ref_to_non_ref.append(citations['refereed to nonrefereed'][k])
        non_ref_to_ref.append(citations['nonrefereed to refereed'][k])
        non_ref_to_non_ref.append(citations['nonrefereed to nonrefereed'][k])

    year_citation, ref_to_ref, ref_to_non_ref, non_ref_to_ref, non_ref_to_non_ref = \
        np.array(year_citation), np.array(ref_to_ref), \
        np.array(ref_to_non_ref), np.array(
            non_ref_to_ref), np.array(non_ref_to_non_ref)
    return year_citation, ref_to_ref, ref_to_non_ref, non_ref_to_ref, non_ref_to_non_ref


def get_numbers_of_papers(metrics):
    """
    Convert the metrics into a format that is easier to work with. Year-ordered
    numpy arrays.
    """
    publications = metrics['histograms']['publications']

    year, total, year_refereed, refereed = [], [], [], []
    y = list(publications['all publications'].keys())
    y.sort()
    for i in range(len(y)):
        k = y[i]
        year.append(datetime.strptime(k, '%Y'))
        total.append(publications['all publications'][k])
        refereed.append(publications['refereed publications'][k])

    year, total, refereed = \
        np.array(year), np.array(total), np.array(refereed)
    return year, total, refereed
