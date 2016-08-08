@shard_2
Feature: CMS.Course updates
    As a course author, I want to be able to provide updates to my students

    # Internet explorer can't select all so the update appears weirdly
    @skip_internetexplorer
    Scenario: Users can change handouts
        Given I have opened a new course in Studio
        And I go to the course updates page
        When I modify the handout to "<ol>Test</ol>"
        Then I see the handout "Test"
        And I see a "saving" notification

# Commenting out as flaky TNL-5051 07/22/2016
#    Scenario: Static links are rewritten when previewing a course update
#       Given I have opened a new course in Studio
#       And I go to the course updates page
#       When I add a new update with the text "<img src='/static/my_img.jpg'/>"
#       # Can only do partial text matches because of the quotes with in quotes (and regexp step matching).
#       Then I should see the asset update to "my_img.jpg"
#       And I change the update from "/static/my_img.jpg" to "<img src='/static/modified.jpg'/>"
#       Then I should see the asset update to "modified.jpg"
#       And when I reload the page
#       Then I should see the asset update to "modified.jpg"

    Scenario: Static links are rewritten when previewing handouts
        Given I have opened a new course in Studio
        And I go to the course updates page
        When I modify the handout to "<ol><img src='/static/my_img.jpg'/></ol>"
        # Can only do partial text matches because of the quotes with in quotes (and regexp step matching).
        Then I see the handout image link "my_img.jpg"
        And I change the handout from "/static/my_img.jpg" to "<img src='/static/modified.jpg'/>"
        Then I see the handout image link "modified.jpg"
        And when I reload the page
        Then I see the handout image link "modified.jpg"

    Scenario: Users cannot save handouts with bad html until edit or update it properly
        Given I have opened a new course in Studio
        And I go to the course updates page
        When I modify the handout to "<p><a href=>[LINK TEXT]</a></p>"
        Then I see the handout error text
        And I see handout save button disabled
        When I edit the handout to "<p><a href='https://www.google.com.pk/'>home</a></p>"
        Then I see handout save button re-enabled
        When I save handout edit
        # Can only do partial text matches because of the quotes with in quotes (and regexp step matching).
        Then I see the handout "https://www.google.com.pk/"
        And when I reload the page
        Then I see the handout "https://www.google.com.pk/"
