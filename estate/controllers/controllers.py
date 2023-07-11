from odoo import http

class Controllers(http.Controller):
    @http.route('/estate',auth='public',website=True)
    def index(self,**kw):
        estate_properties=http.request.env['estate.property']
        return http.request.render('estate.index',{'properties':estate_properties.search([()])
        })
    @http.route(['/properties','/properties/page/<int:page>'],auth='public',website=True)
    def main(self, page=0, items_per_page=6,**kw):
        domain=[('state','in',['new','offer received'])]
        properties=http.request.env['estate.property']
        estate_property_count=properties.search_count([('state','in',['new','offer received'])])
        date=kw.get('date')
        if date:
            domain.append(('date_availability','>=',date))
        pager = http.request.website.pager( 
            url="/properties",
            total=estate_property_count,
            page=page,
            step=items_per_page
        )
        response_property = properties.search(domain,limit=items_per_page, offset=pager['offset']) 
        return http.request.render('estate.main',{
            'properties': response_property, 
            'pager': pager,
        })
        
        Properties = http.request.env['estate.property'].search(domain,limit=4,offset=pager['offset'],order='id desc')
        
        return http.request.render('estate.main', {
             'properties':Properties,
             'pager' : pager,

        })



    @http.route('/properties/<int:id>',auth="public",website=True)
    def property(self, id):
        properties=http.request.env['estate.property']
        return http.request.render('estate.property_template', {
             'properties':properties.search([('id','=',id)])
        })





