"""TO-DO: Write a description of what this XBlock is."""

import pkg_resources
from web_fragments.fragment import Fragment
from xblock.core import XBlock
from xblock.fields import Integer, Scope, Boolean


class MyXBlock(XBlock):
    """
    An XBlock with thumbs-up/thumbs-down voting.

    Vote totals are stored for all students to see.  Each student is recorded
    as has-voted or not.

    This demonstrates multiple data scopes and ajax handlers.

    """
    upvotes = Integer(help="Number of up votes", default=0,
                      scope=Scope.user_state_summary)
    downvotes = Integer(help="Number of down votes", default=0,
                        scope=Scope.user_state_summary)
    voted = Boolean(help="Has this student voted?", default=False,
                    scope=Scope.user_state)

    def resource_string(self, path):
        """Handy helper for getting resources from our kit."""
        data = pkg_resources.resource_string(__name__, path)
        return data.decode("utf8")

    # TO-DO: change this view to display your data your own way.
    def student_view(self, context=None):
        """
        The primary view of the MyXBlock, shown to students
        when viewing courses.
        """
        html = self.resource_string("static/html/myxblock.html")
        frag = Fragment(html.format(self=self))
        frag.add_css(self.resource_string("static/css/myxblock.css"))
        frag.add_javascript(self.resource_string("static/js/src/myxblock.js"))
        frag.initialize_js('MyXBlock')
        return frag

    
    @XBlock.json_handler
    def vote(self, data, suffix=''):  # pylint: disable=unused-argument
        """
        Update the vote count in response to a user action.
        """
        # Here is where we would prevent a student from voting twice, but then
        # we couldn't click more than once in the demo!
        #
        #     if self.voted:
        #         log.error("cheater!")
        #         return

        if data['voteType'] not in ('up', 'down'):
            return None

        if data['voteType'] == 'up':
            self.upvotes += 1
        else:
            self.downvotes += 1

        self.voted = True

        return {'up': self.upvotes, 'down': self.downvotes}

    # TO-DO: change this to create the scenarios you'd like to see in the
    # workbench while developing your XBlock.
    @staticmethod
    def workbench_scenarios():
        """A canned scenario for display in the workbench."""
        return [
            ("MyXBlock",
             """<myxblock/>
             """),
            ("Multiple MyXBlock",
             """<vertical_demo>
                <myxblock/>
                <myxblock/>
                <myxblock/>
                </vertical_demo>
             """),
        ]
