# -*- coding: utf-8 -*-
###############################################################################
#
#    Cybrosys Technologies Pvt. Ltd.
#
#    Copyright (C) 2023-TODAY Cybrosys Technologies(<https://www.cybrosys.com>)
#    Author: Cybrosys Paid App Development Team (odoo@cybrosys.com)
#
#    This program is under the terms of the Odoo Proprietary License v1.0 (OPL-1)
#    It is forbidden to publish, distribute, sublicense, or sell copies of the
#    Software or modified copies of the Software.
#
#    THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#    FITNESS FOR A PARTICULAR PURPOSE AND NON INFRINGEMENT. IN NO EVENT SHALL
#    THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,DAMAGES OR OTHER
#    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,ARISING
#    FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
#    DEALINGS IN THE SOFTWARE.
#
###############################################################################
from odoo import fields, models


class DocumentTrash(models.Model):
    """Module to store deleted documents for a specific time,
    then it automatically"""

    _name = "document.trash"
    _description = "Document Trash"

    name = fields.Char(string="Name", help="Document name")
    attachment = fields.Binary(string="File", readonly=True, help="Document data")
    document_create_date = fields.Datetime(string="Date", help="Document create date")
    workspace_id = fields.Many2one(
        "document.workspace", string="Workspace", required=True, help="workspace name"
    )
    user_id = fields.Many2one(
        "res.users",
        string="Owner",
        default=lambda self: self.env.user,
        help="""owner name, if the document belongs to a specific user""",
    )
    brochure_url = fields.Char(string="URL", store=True, help="Document sharable URL")
    extension = fields.Char(string="Extension", help="helps to determine the file type")
    priority = fields.Selection(
        selection=[("0", "None"), ("1", "Favorite")],
        string="Priority",
        help="Favorite button",
    )
    attachment_id = fields.Many2one(
        "ir.attachment",
        string="Attachment",
        help="Used to access datas without search function",
    )
    content_url = fields.Char(
        string="Content Url", help="It store the URL for url type documents"
    )
    content_type = fields.Selection(
        [("file", "File"), ("url", "Url")],
        help="Document content type",
        string="Content type",
    )
    preview = fields.Char(
        string="Preview", help="Used to show a preview for URL file type"
    )
    active = fields.Boolean(
        string="Active", default=True, help="It specify archived file"
    )
    days = fields.Integer(string="Days", help="auto delete in days")
    deleted_date = fields.Date(string="Deleted Date", help="File deleted date")
    mimetype = fields.Char(string="Mime Type", help="Document mimetype")
    description = fields.Text(string="Description", help="Short description")
    security = fields.Selection(
        string="Security",
        selection=[
            ("private", "Private"),
            ("managers_and_owner", "Managers & Owner"),
            ("specific_users", "Specific Users"),
        ],
        default="managers_and_owner",
        help="""Privet : only the uploaded user can view
                    Managers & Owner : Document shared with Managers """,
    )
    user_ids = fields.Many2many(
        "res.users", help="Can access the documents", string="User Access"
    )
    partner_id = fields.Many2one(
        "res.partner", help="Document related partner name", string="Related Partner"
    )
    auto_delete = fields.Boolean(
        string="Auto Delete", default=False, help="Document delete status"
    )
    delete_date = fields.Date(
        string="Date Delete",
        readonly=True,
        help="Used to calculate file remove date from trash",
    )
    file_url = fields.Char(
        string="File URL", help="""it store url while adding an url document"""
    )
    size = fields.Char(string="Size", help="it store size of the document")
    company_id = fields.Many2one(
        related='workspace_id.company_id', string='Company',
        help="Company Name")

    def delete_doc(self):
        """Function to delete all the documents after the trash date"""
        trash_limit = (
            self.env["ir.config_parameter"]
            .sudo()
            .get_param("document_management.trash")
        )
        if trash_limit:
            for rec in self.search([]):
                if fields.Date.today() == fields.Date.add(
                    rec.deleted_date, days=int(trash_limit)
                ):
                    rec.unlink()
