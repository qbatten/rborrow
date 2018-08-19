import sys
from lark import Lark, Transformer, v_args



grammar = r'''
            _title: "[" ptype  _spacing r_amt _spacing r_loc _spacing  r_gen  _spacing ( r_type ( _spacing? r_misc? ( ")" | "]" )? )? )?
                 | "[" ptype _spacing p_user _spacing p_amt _spacing p_timing ( ")" | "]" )?
                 | "[" ptype _spacing u_user _spacing u_loc _spacing u_amt _spacing? u_timing? _spacing? u_misc? ( ")" | "]" )?
                 | "[" ptype _spacing m_misc
 
        // Post Types

             ptype: REQ
                 | PAID
                 | UNPAID
                 | META

              REQ: "REQ" | "Req" | "req" 
             PAID:  "PAID" 
           UNPAID: "UNPAID" 
            META :  "META"


        // Requests

            r_amt: _cash -> r_amount

            r_loc: "#" (/[A-Za-z0-9#]+/ _SPACERS? )+ -> location 
 
            r_gen: date? /[A-Za-z0-9\$€£\s\/',.@%+&-]+/? date?      //# /[A-Za-z\$£,][^\)\]]*/? date?

           r_type: _w_gobbler

           r_misc: _w_gobbler


        // Paid

           p_user: user

            p_amt: amt

         p_timing: _w_gobbler


        // Unpaid

           u_user: user

            u_loc: loc

            u_amt: amt

           u_misc: _w_gobbler

         u_timing: _w_gobbler

        // Meta

            m_misc: _w_gobbler

        // General Use Rules

        _w_gobbler: /[0-9A-Za-z!\/\s\$'?,.&;-]+/

              amt: _cash /[+]/? ( _cash | /[A-Za-z]+/ )?

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

           user.2: "/u/" /[A-Za-z0-9_\-]+/
                 | user_bad
         user_bad: "u/" /[A-Za-z0-9_\-]+/
                 |  "/u" /[A-Za-z0-9_\-]+/
                 |  "/" /[A-Za-z0-9_\-]+/




           _cash.2: _MONEY INT | INT _MONEY
                 |  _cash_bad
         _cash_bad: /[$£€]/? INT /[€\.-]/? ( /[A-Za-z\-\/,]+/ | /[$£]/? /[0-9\.-]+/ )*
         _spacing: _spacing_ok
                 | _spacing_bad
                 | _spacing_xbad
    _spacing_ok.3: _bclose _SPACERS? _bopen
    _spacing_bad.2: _bclose _SPACERS? _bopen?
     _spacing_xbad: _bclose? _SPACERS? _bopen?
           _bopen: ( "[" | "(" )
          _bclose: ( "]" | ")" )
 
           STRING: STRING_INNER
           _MONEY: /[$€£]
         _SPACERS: ("-" | "," | ".")
 
                %import common.STRING_INNER
                %import common.INT
                %import common.WS
                %ignore WS
                %ignore "\\u00a3"
                %ignore "\\u20ac"
 
            '''

def outtest(t, out={}, tmpkey=0):
    if isinstance(t, lark.Tree):
        for i, elem in enumerate(t.children):
            if not t.data == "_title":
                print(t.data + "||")
                tmpkey = t.data
            outtest(elem, out, tmpkey)
    else:
        out[tmpkey] = t[:]
        print(t[:])

    return(out)


