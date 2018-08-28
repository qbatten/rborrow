import lark
import json


grammar = r'''
            ptype: "["? REQ  _spacing r_amt _spacing r_loc _spacing  r_gen  _spacing ( r_type ( _spacing? r_misc? ( ")" | "]" )? )? )?
                 | "["? PAID _spacing p_user _spacing p_amt (_spacing (p_timing ( ")" | "]" )?)?)?
                 | "["? UNPAID _spacing u_user _spacing u_loc _spacing u_amt _spacing? u_timing? _spacing? u_misc? ( ")" | "]" )?
                 | "["? META _spacing m_misc

        // Post Types

              REQ: "REQ" | "Req" | "req"
             PAID:  "PAID"
           UNPAID: "UNPAID"
            META :  "META"


        // Requests

            r_amt: _cash -> r_amt

            r_loc: "#" (/[A-Za-z0-9#]+/ _SPACERS? )+ -> location

            r_gen: date? /[A-Za-z0-9\$€£\s\/',.@%+&-]+/? date?      //# /[A-Za-z\$£,][^\)\]]*/? date?

           r_type: _w_gobbler

           r_misc: _w_gobbler


        // Paid

           p_user: _user

            p_amt: _amt -> p_amt

         p_timing: _w_gobbler


        // Unpaid

           u_user: _user

            u_loc: loc

            u_amt: _amt -> u_amt

           u_misc: _w_gobbler

         u_timing: _w_gobbler

        // Meta

            m_misc: _w_gobbler

        // General Use Rules

        _w_gobbler: /[0-9A-Za-z!\/\s\$'?,.&;-]+/

              _amt: _cash /[+]/? ( _cash | /[A-Za-z]+/ )?

             date: dnum
                 | dword
             dnum: /[0-9]{1,2}[\/\-.]?/+
            dword: mon ( _SPACERS | "/" )? day ( _SPACERS | "/" )? yr?
                 | day ( _SPACERS | "/" | "of" )? mon ( _SPACERS | "/" )? yr?
              day: /[0-9]{1,2}[ts]?[ht]?/
              mon: dm_num | dm_word
          dm_num: /[0-9][0-2]?/
          dm_word: "Jan" | "Feb" | "Mar" | "Apr" | "May" | "Jun" | "Jul" | "Aug" | "Sept" | "Nov" | "Dec"
                 | "January" | "February" | "March" | "April" | "May" | "June" | "July" | "August" | "September" | "November" | "December"
                 | "jan" | "feb" | "mar" | "apr" | "may" | "jun" | "jul" | "aug" | "sept" | "nov" | "dec"
                 | "january" | "february" | "march" | "april" | "may" | "june" | "july" | "august" | "september" | "november" | "december"
               yr: /[12][0-9][0-9]?[0-9]?/



              loc: "#" (/[A-Za-z.0-9#]+/ _SPACERS? )+

             _user: _user_good | _user_bad
     _user_good.2: "/u/" /[A-Za-z0-9_\-]+/
        _user_bad: "u/" /[A-Za-z0-9_\-]+/
                 |  "/u" /[A-Za-z0-9_\-]+/
                 |  "/" /[A-Za-z0-9_\-]+/




           _cash.2: _MONEY INT | INT _MONEY
                 |  _cash_bad
         _cash_bad: /[$£€]/? INT /[£$€\.-]/? ( /[A-Za-z\-\/,]+/ | /[$£]/? /[0-9\.-]+/ )*
         _spacing: _spacing_ok
                 | _spacing_bad
                 | _spacing_xbad
    _spacing_ok.3: _bclose _SPACERS? _bopen
    _spacing_bad.2: _bclose _SPACERS? _bopen?
     _spacing_xbad: _bclose? _SPACERS? _bopen?
           _bopen: ( "[" | "(" )
          _bclose: ( "]" | ")" )

           STRING: STRING_INNER
           _MONEY: /[$€£]/
         _SPACERS: ("-" | "," | ".")

                %import common.STRING_INNER
               %import common.INT
                %import common.WS
                %ignore WS
                %ignore "\\u00a3"
                %ignore "\\u20ac"
'''

def treeToDict(t, out={}, tmpkey='ptype'):
    '''Takes our Lark tree and turns it into a useful dict
    '''
    if isinstance(t, lark.Tree):
        for i, elem in enumerate(t.children):
            tmpkey = t.data
            treeToDict(elem, out, tmpkey)

    else:
        out[tmpkey] = t[:]

    return out


def parseTitle(to_parse):
    '''Calls our grammar and parses the title, outputting a Lark tree
    '''
    title_parser = lark.Lark(grammar, start="ptype")
    out = treeToDict(title_parser.parse(to_parse), out={})
    return out


def readfile(fin="/Users/quinnbatten/Documents/Programming/PyProjects/rborrow/main1.json"):
    ''' Generic JSON reader, defaults to calling the file that getdata() outputs
    '''

    with open(fin) as f:
        vals = json.load(f)
    return vals



def getgraphinmem():
    '''Helper that reads our netdict file (the data translated into a useful dictionary thingie.)
    '''
    netdict = readfile("/Users/quinnbatten/Documents/Programming/PyProjects/rborrow/netdict1.txt")

    return netdict


def parse_indict(indict):
    output = []
    i = 0
    for post in indict:
        i += 1
        currPost = {}

        # Parse titles
        try:
            tmp = parseTitle(post['title'])
        except Exception as inst:
           # print(str(i) + " || Exc! type: " + str(inst))
            tmp = {'parseErr' : str(inst)}
        else:
           # print(i)
            currPost.update({'parseErr' : False})
        finally:
            currPost.update(tmp)

        currPost['author'] = post['author']
        currPost['date'] = post['created_utc']
        currPost['url'] = post['full_link']
        currPost['title'] = post['title']
        if 'selftext' in post:
            currPost['body'] = post['selftext']
        else:
            currPost['body'] = ''
        currPost['score'] = post['score']
        currPost['postid'] = post['id']

        if i % 100 == 0:
            print(i)
        output.append(currPost)
    return output


