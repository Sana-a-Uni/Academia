# Copyright (c) 2024, SanU and contributors
# For license information, please see license.txt

import uuid
from academia.councils.doctype.council.council import validate_members
import frappe
from frappe.model.document import Document
from frappe.utils import nowdate
from frappe.utils import getdate

from frappe import _
import locale
from jinja2 import Template
import json
from datetime import datetime


class Session(Document):
    # begin: auto-generated types
    # This code is auto-generated. Do not modify anything in this block.

    from typing import TYPE_CHECKING

    if TYPE_CHECKING:
        from academia.councils.doctype.session_member.session_member import SessionMember
        from academia.councils.doctype.session_topic.session_topic import SessionTopic
        from frappe.types import DF

        amended_from: DF.Link | None
        begin_time: DF.Time | None
        council: DF.Link
        date: DF.Date | None
        end_time: DF.Time | None
        members: DF.Table[SessionMember]
        naming_series: DF.Literal["CNCL-SESS-.YY.-.{council}.-.###"]
        opening: DF.TextEditor | None
        title: DF.Data
        topics: DF.Table[SessionTopic]
    # end: auto-generated types

    def validate(self):
        self.validate_time()
        validate_members(self.members)
        self.validate_topics()
        self.validate_topic_duplicate()

    def detect_topics_changes(self):
        """
        This function compares the current session's topics with the old session's topics(before save),
        and returns a list of edited topics, a list of added topics, and a list of deleted topics.

        Returns:
            tuple: A tuple containing three lists: edited topics, added topics, and deleted topics.

        """
        # Check if this is a new session (no previous session to compare with)
        if self.is_new():
            return [], [], []

        # Get the previous session's topics
        old_session = self.get_doc_before_save()
        old_topics = {
            row.name: row for row in old_session.topics} if old_session else {}

        # Get the current session's topics as dictionary and set name as key
        current_topics = {row.name: row for row in self.topics}

        # Find deleted topics (topics present in old session but not in current session)
        deleted_topics = [
            row for row in old_session.topics if row.name not in current_topics]

        # Find added topics (topics present in current session but marked as new)
        added_topics = [row for row in self.topics if row.is_new()]

        # Initialize a list to store edited topics
        edited_topics = []

        # Iterate through the current session's topics
        for row_name, topic_doc in current_topics.items():
            # Check if the topic exists in the old session and is not marked as new
            if row_name in old_topics and not topic_doc.is_new():
                # Get the old topic document
                old_topic_doc = old_topics[row_name]

                # Compare the modified status of the old and current topics
                if old_topic_doc.modified != topic_doc.modified:
                    # If the modified status is different, add the topic to the edited topics list
                    edited_topics.append(topic_doc)

        # Return the lists of edited, added, and deleted topics
        return edited_topics, added_topics, deleted_topics

    # def create_postponed_topic(self, session_topic):
    # 	"""Creates a new Topic topic with postponed status the specified details.

    # 	Args:
    # 	        session_topic (Session.topics): The session topic details.
    # 	Returns:
    # 	        Document: The newly created Topic document.
    # 	"""
    # 	doc_topic = frappe.new_doc("Topic")
    # 	doc_topic.title = session_topic.title
    # 	doc_topic.description = session_topic.description
    # 	doc_topic.topic_date = (nowdate(),)
    # 	doc_topic.council = session_topic.council
    # 	# doc_assignment.topic = session_assignment.topic
    # 	doc_topic.status = "Accepted"
    # 	doc_topic.insert()
    # 	return doc_topic

    def on_submit(self):
        self.process_session_topics()

    def before_save(self):
        self.update_topics_status()
        self.minute_hash = 'SM-'+str(uuid.uuid1())


    def process_session_topics(self):
        """
        Process each session topic, create new topics for postponed topics,
        and update existing topic  with decision details.
        """
        # Retrieve session topics from the document
        session_topics = self.topics

        # Process each session topic
        for session_topic in session_topics:
            # Retrieve details of the corresponding Topic
            session_topic_doc = frappe.get_doc("Topic", session_topic.topic)

            # # If the decision type is "Postponed":
            # if session_topic.decision_type == "Postponed":
            # 	# Create a new topic for postponed topics
            # 	if session_topic_doc:
            # 		self.create_postponed_topic(session_topic)

            # self.process_council_memo(session_topic)

            # Update the Topic with the decision details
            session_topic_doc.decision = session_topic.decision
            session_topic_doc.status = session_topic.status
            session_topic_doc.decision_type = session_topic.decision_type
            session_topic_doc.save()
            session_topic_doc.submit()

    # def process_council_memo(self, session_assignment):
    # 	if session_assignment.council_memo:
    # 		if session_assignment.decision_type == "Transferred":
    # 			doc = frappe.get_doc("Council Memo", session_assignment.council_memo)
    # 			# Updating the Status and Getting Sent Date
    # 			doc.status = "Verified"
    # 			doc.sent_date = getdate()
    # 			doc.save()
    # 			# ----------------------------------------
    # 			doc.submit()
    # 		else:
    # 			frappe.db.set_value("Session Topic Assignment", session_assignment.name, "council_memo", "")
    # 			frappe.db.delete("Council Memo", {"name": session_assignment.council_memo})
    def update_topics_status(self):
        _, added_topics, deleted_topics = self.detect_topics_changes()
        for session_topic in added_topics:
            frappe.db.set_value("Topic",
                                session_topic.topic, "status", "Scheduled")
        for session_topic in deleted_topics:
            frappe.db.set_value("Topic",
                                session_topic.topic, "status", "Pending")

    def validate_time(self):
        if self.begin_time and self.end_time:
            if self.begin_time > self.end_time:
                frappe.throw(_("End time must be after begin time"))

    def validate_topic_duplicate(self):
        topics = [row.topic for row in self.topics]
        topics_set = set(topics)
        if len(topics) != len(topics_set):
            frappe.throw(_("Topics can't be duplicated"))

    def validate_topics(self):
        for row in self.topics:
            topic = frappe.get_value("Topic", row.topic, ["*"], as_dict=1)
            if not (
                    topic.docstatus == 0
                    and topic.council == self.council
                    and topic.status == "Pending"
                    and not topic.parent_topic
            ):
                frappe.throw(
                    _("There are topic outside the valid list, please check again."))


@frappe.whitelist()
def get_template(decision_template=None, topic=None, session=None):
    try:
        decision_template_id = get_decision_template_id(
        ) if not decision_template else decision_template
        decision_template_data = fetch_decision_template(decision_template_id)
        if not decision_template_data:
            return None

        topic_info = fetch_topic_info(topic) if topic else None
        if session:
            session_data = json.loads(session)
        else:
            return None
        attendees, absentees = extract_session_members(session_data)
        session_data["weekday"] = extract_weekday_from_date(
            session_data["date"])
        # Convert the string to a datetime object
        rendered_template = render_decision_template(
            decision_template_data, topic_info, attendees, absentees, session_data
        )
        return rendered_template

    except Exception as e:
        log_and_return_error(e)


def get_decision_template_id():
    decision_template = frappe.get_all(
        "Topic Decision Template", filters={"subject": "افتتاحية الجلسة"}, fields=["name"]
    )
    if not decision_template:
        return None
    return decision_template[0].name


def fetch_decision_template(decision_template_id):
    if not decision_template_id:
        return None
    return frappe.get_doc("Topic Decision Template", decision_template_id)


def fetch_topic_info(topic):
    topic_docs = frappe.get_doc("Topic", topic)
    if not topic_docs:
        return None
    return topic_docs.as_dict()


def extract_session_members(session_data):
    attendees = []
    absentees = []
    if "members" in session_data:
        for member in session_data["members"]:
            member_info = {"name": member.get(
                "member_name", ""), "role": member.get("member_role", "")}
            if member.get("attendance") == "Attend":
                attendees.append(member_info)
            else:
                absentees.append(member_info)
    return attendees, absentees


def render_decision_template(decision_template_data, topic_info, attendees, absentees, session_data):
    template_content = decision_template_data.decision
    template = Template(template_content)

    return template.render(
        topic=topic_info if topic_info else {}, attendees=attendees, absentees=absentees, session=session_data
    )


def extract_weekday_from_date(date_str):
    # Set the locale to Arabic for Gregorian date
    locale.setlocale(locale.LC_TIME, "ar_SA.utf8")

    date_obj = datetime.strptime(date_str, "%Y-%m-%d")

    weekday = date_obj.strftime("%A")

    return weekday


def log_and_return_error(exception):
    frappe.log_error(frappe.get_traceback(),
                     "Error fetching Decision Template")
    return {"error": str(exception)}
