from bakery import assert_equal
from drafter import *
from dataclasses import dataclass
from random import sample, shuffle

set_website_title("Boardom Buster")
set_site_information(
    author="Elizabeth Davis",
    description="Discover new hobbies and overcome boredom.",
    sources="Thanks to the Drafter docs.",
    planning=["Final Project 0_ Pick a Problem.pdf", "CS1 Final Project 1_Design.pdf,LLM Conversation.pdf",],
    links=["https://github.com/ElizabethDavis15/Boredom-Buster"]
)
hide_debug_information()
set_website_framed(False)

@dataclass
class Activity:
    """Represents a single activity."""
    title: str
    mood: str
    location: str
    setting: str
    cost: int

@dataclass
class State:
    """State containing user preferences and activity list."""
    selected_mood: str
    budget_max: int
    selected_group: str
    selected_location: str
    browse_location: str
    browse_mood: str
    browse_setting: str
    browse_cost: int
    activities: list[Activity]

INITIAL_ACTIVITIES: list[Activity] = [
    Activity("Board Game Night", "Medium", "At Home", "Group", 20),
    Activity("DIY Mug Painting", "Low", "At Home", "Solo/Group", 15),
    Activity("Trail Hiking", "High", "Outdoor", "Solo/Group", 0),
    Activity("Bake Chocolate Chip Cookies", "Low", "At Home", "Solo/Group", 10),
    Activity("Local Museum Tour", "Low", "Indoor", "Solo/Group", 15),
    Activity("Frisbee Golf", "High", "Outdoor", "Group", 10),
    Activity("Indoor Rock Climbing", "High", "Indoor", "Solo/Group", 30),
    Activity("Podcast & Stroll", "Low", "Outdoor", "Solo", 0),
    Activity("Learn a Magic Trick", "Low", "At Home", "Solo", 5),
    Activity("Park Picnic", "Low", "Outdoor", "Group", 20),
    Activity("Origami Challenge", "Low", "At Home", "Solo", 5),
    Activity("Bowling Session", "Medium", "Indoor", "Group", 25),
    Activity("At-Home Spa Night", "Low", "At Home", "Solo/Group", 15),
    Activity("Neighborhood Scavenger Hunt", "Medium", "Outdoor", "Group", 0),
    Activity("Learn an Online Dance Routine", "High", "At Home", "Solo/Group", 0),
    Activity("Visit a Local Farmers Market", "Low", "Outdoor", "Solo/Group", 25),
    Activity("DIY Tie-Dye Shirts", "Medium", "Outdoor", "Solo/Group", 20),
    Activity("Arcade Games Night", "Medium", "Indoor", "Solo/Group", 30),
    Activity("Stargazing with an App", "Low", "Outdoor", "Solo/Group", 0),
    Activity("Home Workout Routine", "High", "At Home", "Solo", 0),
    Activity("Try a New Coffee Shop", "Low", "Indoor", "Solo/Group", 10),
    Activity("Plant an Indoor Herb Garden", "Low", "At Home", "Solo", 25),
    Activity("Escape Room Experience", "Medium", "Indoor", "Group", 40),
    Activity("Build a Fort & Movie Marathon", "Low", "At Home", "Solo/Group", 5),
    Activity("Bicycle Trail Ride", "High", "Outdoor", "Solo/Group", 0),
    Activity("Learn a New Card Game", "Low", "At Home", "Solo/Group", 5),
    Activity("Visit a Public Library", "Low", "Indoor", "Solo", 0),
    Activity("DIY Candle Making", "Medium", "At Home", "Solo/Group", 30),
    Activity("Beach or Lake Day", "Medium", "Outdoor", "Solo/Group", 10),
    Activity("Call an Old Friend", "Low", "At Home", "Solo", 0),
    Activity("Photography Walk", "Medium", "Outdoor", "Solo", 0),
    Activity("Miniature Golf", "Low", "Outdoor", "Group", 15),
    Activity("Write a Short Story", "Low", "At Home", "Solo", 0),
    Activity("Karaoke at Home", "High", "At Home", "Group", 0),
    Activity("Visit a Thrift Store", "Low", "Indoor", "Solo/Group", 20),
    Activity("Jump Rope Challenge", "High", "Outdoor", "Solo", 10),
    Activity("Watercolor Painting", "Low", "At Home", "Solo", 15),
    Activity("Ice Skating", "High", "Indoor", "Solo/Group", 20),
    Activity("Cook a Foreign Cuisine Recipe", "Medium", "At Home", "Solo/Group", 35),
    Activity("Geocaching Adventure", "Medium", "Outdoor", "Solo/Group", 0),
    Activity("Organize & Declutter a Room", "Medium", "At Home", "Solo", 0),
    Activity("Outdoor Yoga Session", "Low", "Outdoor", "Solo/Group", 0),
    Activity("Go to a Matinee Movie", "Low", "Indoor", "Solo/Group", 15),
    Activity("Create a Vision Board", "Low", "At Home", "Solo", 10),
    Activity("Roller Skating", "High", "Outdoor", "Solo/Group", 15),
    Activity("Learn Basic Calligraphy", "Low", "At Home", "Solo", 15),
    Activity("Visit an Aquarium", "Low", "Indoor", "Solo/Group", 45),
    Activity("Make Homemade Pizza", "Medium", "At Home", "Solo/Group", 20),
    Activity("Bird Watching at a Park", "Low", "Outdoor", "Solo", 0),
    Activity("Puzzle Marathon", "Low", "At Home", "Solo/Group", 15),
]

initial_state = State(
    "Medium", 25, "Solo", "At Home",
    "All", "All", "All", 50,
    list(INITIAL_ACTIVITIES)
)

def helper_filter(activities: list[Activity], mood: str, budget: int, group: str, location: str) -> list[Activity]:
    """Filter activities based on mood, budget, group or solo, and location."""
    filtered: list[Activity] = []
    for act in activities:  
        mood_match = (act.mood == mood)
        budget_match = (act.cost <= budget)
        location_match = (act.location == location)
        group_match = (
            group in act.setting 
            or act.setting == "Solo/Group" 
            or group == "Both"
        )
        
        if mood_match and budget_match and location_match and group_match:
            filtered.append(act)
    return filtered

assert_equal(
    helper_filter(INITIAL_ACTIVITIES, "Low", 5, "Solo", "At Home"),
    [Activity(title='Learn a Magic Trick', mood='Low', location='At Home', setting='Solo', cost=5),
     Activity(title='Origami Challenge', mood='Low', location='At Home', setting='Solo', cost=5),
     Activity(title='Build a Fort & Movie Marathon', mood='Low', location='At Home', setting='Solo/Group', cost=5),
     Activity(title='Learn a New Card Game', mood='Low', location='At Home', setting='Solo/Group', cost=5),
     Activity(title='Call an Old Friend', mood='Low', location='At Home', setting='Solo', cost=0),
     Activity(title='Write a Short Story', mood='Low', location='At Home', setting='Solo', cost=0)]
)

def helper_matches(act_setting: str, filter_setting: str) -> bool:
    """Determine if an activity setting matches the active filter setting."""
    if filter_setting == "All":
        return True
    if filter_setting == "Solo" and "Solo" in act_setting:
        return True
    if filter_setting == "Group" and "Group" in act_setting:
        return True
    return act_setting == filter_setting

assert_equal(helper_matches("Solo", "Solo"), True)
assert_equal(helper_matches("Group", "Solo"), False)

def helper_index() -> list:
    """Generate standard header buttons for application pages."""
    return [
        Header("BOREDOM BUSTER", 1),
        Paragraph("Stuck for things to do? Find your ideal activity."),
        Button("Home", "index"),
        Button("About", "about"),
        Button("Finder", "finder"),
        Button("Browse", "browse"),
        Button("FAQ", "faq"),
        Button("Contact", "contact"),
        HorizontalRule(),
    ]

assert_equal(len(helper_index()), 9)
assert_equal(helper_index()[0], Header("BOREDOM BUSTER", 1))

@route
def index(state: State) -> Page:
    """Display the home page of the Boredom Buster application."""
    nav = helper_index()
    content = [
        *nav,
        Header("Welcome to Boredom Buster", 2),
        Paragraph("Discover new hobbies and overcome boredom."),
        Button("Get Started", "finder"),
    ]
    return Page(state, content)

assert_equal(type(index(initial_state)), Page)

@route
def about(state: State) -> Page:
    """Display the about page explaining the application purpose."""
    nav = helper_index()
    content = [
        *nav,
        Header("About Boredom Buster", 2),
        Paragraph("Helps users discover activities based on mood, budget, and setting."),
    ]
    return Page(state, content)

assert_equal(type(about(initial_state)), Page)

@route
def contact(state: State) -> Page:
    """Display the contact support page."""
    nav = helper_index()
    content = [
        *nav,
        Header("Contact Us", 2),
        Paragraph("Have questions? Reach out to egdavis@udel.edu"),
    ]
    return Page(state, content)

assert_equal(type(contact(initial_state)), Page)

@route
def faq(state: State) -> Page:
    """Display frequently asked questions regarding application usage."""
    nav = helper_index()
    content = [
        *nav,
        Header("Frequently Asked Questions", 2),
        Paragraph("Q1: Is this application completely free to use?"),
        Paragraph("A1: Yes, Boredom Buster is 100% free for exploring activities."),
        Paragraph("Q2: How do I filter activities by my budget?"),
        Paragraph("A2: Use the Personal Activity Finder to type your maximum budget."),
        Paragraph("Q3: Can I find activities to do with friends?"),
        Paragraph("A3: Yes, select 'Group' or 'Both' under the Social Setting option."),
        Paragraph("Q4: Are all suggested activities suitable for beginners?"),
        Paragraph("A4: Absolutely! Most activities require no prior experience."),
        Paragraph("Q5: How do I reset or change my preferences?"),
        Paragraph("A5: Simply go back to the Finder tab and update your selections."),
    ]
    return Page(state, content)

assert_equal(type(faq(initial_state)), Page)

@route
def finder(state: State) -> Page:
    """Display the Personal Activity Finder page with interactive form inputs."""
    nav = helper_index()
    content = [
        *nav,
        Header("Personal Activity Finder", 2),
        Paragraph("Tell us what you like:"),
        SelectBox("mood_input", ["Low", "Medium", "High"], state.selected_mood),                    
        TextBox("budget_input", str(state.budget_max)),   
        SelectBox("group_input", ["Solo", "Group", "Both"], state.selected_group),                    
        SelectBox(
            "location_input", 
            ["At Home", "Indoor", "Outdoor"], 
            state.selected_location
        ),                    
        Button("View Recommendations", "recommendation"),
    ]
    return Page(state, content)

assert_equal(type(finder(initial_state)), Page)

@route
def browse(state: State, loc_input: str = "All", mood_inp: str = "All", set_inp: str = "All", cost_inp: str = "50") -> Page:
    """Filter and display all activities based on browse preferences."""
    state.browse_location = loc_input  
    state.browse_mood = mood_inp
    state.browse_setting = set_inp
    if cost_inp.isdigit():
        state.browse_cost = int(cost_inp)
    else:
        state.browse_cost = 50

    shuffle(state.activities)

    filtered_activities = []
    for act in state.activities:  
        loc_match = (
            state.browse_location == "All" 
            or act.location == state.browse_location
        )
        mood_match = (
            state.browse_mood == "All" 
            or act.mood == state.browse_mood
        )
        setting_match = helper_matches(act.setting, state.browse_setting)
        cost_match = (act.cost <= state.browse_cost)

        if loc_match and mood_match and setting_match and cost_match:
            filtered_activities.append(act)
    table_rows: list[list[Component|str|int|float|bool]]=[
        ["Name","location","Mood","setting","Cost"]
    ]
    for act in filtered_activities:
        table_rows.append([act.location, act.mood, act.setting, act.cost])

    nav = helper_index()
    content = [
        *nav,
        Header("Browse Activities", 2),
        Paragraph(f"Found {len(filtered_activities)} matching activities."),
        SelectBox(
            "loc_input", 
            ["All", "At Home", "Indoor", "Outdoor"], 
            state.browse_location
        ),
        SelectBox(
            "mood_inp", 
            ["All", "Low", "Medium", "High"], 
            state.browse_mood
        ),
        SelectBox(
            "set_inp", 
            ["All", "Solo", "Group"], 
            state.browse_setting
        ),
        TextBox("cost_inp", str(state.browse_cost)),
        Button("Apply Filters", "browse"),
        Table(table_rows),
        Button("Back to Finder", "finder"),
    ]
    return Page(state, content)

assert_equal(type(browse(initial_state, "All", "All", "All", "50")), Page)

@route
def recommendation(state:State,mood_input:str,budget_input:str,group_input:str,location_input:str)->Page:
    """
    Process user search filters from page finder, update the state dataclass, and display a randomized recommendation.
    Note: Due to randomization, this route is exempt from testing.
    """
    state.selected_mood = mood_input        
    state.selected_group = group_input        
    state.selected_location = location_input  
    state.budget_max = int(budget_input)      

    nav = helper_index()
    matched = helper_filter(
        state.activities, 
        state.selected_mood, 
        state.budget_max, 
        state.selected_group, 
        state.selected_location
    )
    
    if len(matched) > 0:
        chosen_activity = sample(matched, 1)[0]
        rec_text = chosen_activity.title
    else:
        rec_text = "No exact match found for your specific combination."

    content = [
        *nav,
        Header("Your Activity Recommendation", 2),
        Paragraph(rec_text),
        Button("Back to Finder", "finder"),
        Button("Browse All", "browse"),
    ]
    return Page(state, content)


if __name__ == "__main__":
    start_server(initial_state)
