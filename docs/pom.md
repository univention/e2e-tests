# Page Object Model

## Overview

We use the Page Object Model (POM) for representing webpages.
You can find the Page Objects (POs) under `src/umspages` in this
repository.

Here are some useful links for reading about POM basic concepts.

1. [A general introduction to POM](https://martinfowler.com/bliki/PageObject.html)
2. [POM implementation using Selenium](https://selenium-python.readthedocs.io/page-objects.html)
3. [POM implementation using Playwright](https://playwright.dev/python/docs/pom)

The basic implementations outlined above are inadequate for our use case for two important reasons.

1. Both the Selenium and Playwright implementations are too basic for modern
   webpages with many elements. We need a POM that can handle complexity while
   keeping the classes maintainable (more on that later).

2. I have come across POM implementations in Selenium that are more capable of
   handing complex web pages (though there isn't a standard one). One could try to
   port such an implementation to Playwright. However, I think this is a bad idea
   because these implementations were designed with Selenium in mind.
   Playwright is fundamentally different from Selenium in many ways. Therefore,
   I believe it is better to build a POM from scratch so that it integrates well
   with the Playwright way of doing things.

With that in mind, we have developed our own custom POM jumping off from the
basic POM implementation in the Playwright docs.

The POM example in the Playwright docs can represent a page containing flat
list of elements as shown in the code below. Here, we are trying to represent
a web page with a header and a sidebar. (Note that in the following code
examples, we will use the `.locator()` method to represent any Playwright
locator method).

```
class ExamplePage:
    def __init__(self, page):
        self.page = page
        self.header_element_1 = self.page.locator(...)
        self.header_element_2 = ...
        ...
        self.sidebar_element_1 = ...
        self.sidebar_element_2 = ...
        ...
        self.page_specific_element_1 = ...
        self.page_specific_element_2 = ...
        ...

    # Header related operations
    def header_element_1_operation():
       ...

    ...

    # Sidebar related operations

    def sidebar_element_1_operation():
       ...

    ...

    # Page specific element operation

    def page_specific_element_1_operation():
       ...

    ...
```

However, modern web pages contain so many elements that putting all of these
elements and their related operations under the same page object leads to
bloated POs. It is better to separate out *logical collections of elements*
(aka **page parts**) and related operations into other classes.

```
class ExamplePage:
    def __init__(self, page):
        self.page = page
        self.header = Header(self.page.locator(...))
        self.sidebar = Sidebar(self.page.locator(...))
        self.page_specific_element_1 = ...
        self.page_specific_element_2 = ...
        ...

    # Page specific element operation

    def page_specific_element_1_operation():
       ...

    ...

class Header:  # This is a page part
    def __init__(self, locator):
        self.locator = locator
        self.header_element_1 = self.locator.locator(...)  # Uses Playwright's locator chaining
        self.header_element_2 = ...

    # Header related operations
    def header_element_1_operation():
       ...

    ...

class Sidebar:  # Another page part
    ...
```



The classes representing a full webpage (`ExamplePage`) and the classes
representing a page part (`Header`, `Sidebar`) shouldn't be treated on the
same footing, because a full webpage is determined by either a URL or a
certain navigation path, while a page part depends on a locator relative to a
parent. This is a fundamental distinction, which we also make apparent in the
signature of the `__init__()` methods of the two types of classes
(one accepts a Playwright `Page` and the other accepts a Playwright `Locator`).

Therefore, in our `pages` packages, we define two different base classes, one
for representing full webpages (`BasePage`) and one for representing page parts (`BasePagePart`).

These base classes can be found under `pages/base.py`. Here's the full list of base classes.

| Class | Purpose |
| --- | --- |
| `BasePage` | Represents a full webpage. Any class trying to represent a full webpage should derive from this class. |
| `BasePagePart` | Represents a page part e.g. a navigation header that appears in many pages in the webapp under test. Any class trying to represent a page part should derive from this class. |

You should define your own concrete Page Objects as follows.

```
from playwright.sync_api import Page

class HomePage(BasePage):
    def set_content(self, page: Page):
        # The super call makes the self.page instance attribute available
        super().set_content(page)
        # self.page can be used to locate elements on the page
        self.example_element = self.page.locator(...)

    def navigate():
        """A method to navigate to the webpage.
        Implementation is not enforced, but recommended.
        """

    def is_displayed():
        """A method to check the the Playwright Page we are currently on is indeed this page
        Implementation by child classes is not enforced, but recommended
        """

    ...
```

You should define your own concrete Page Parts as follows.

```
from playwright.sync_api import Locator

class Header(BasePagePart):
    def __init__(self, page_part_locator: Locator):
        # The super() call makes the self.page_part_locator instance attribute avaialable
        super().__init__(page_part_locator)
        # self.page_part_locator can be used to locate elements inside the page part
        self.subelement = self.page_part_locator.locator(...)

    ...
```

## More on Page Parts

### How to use Page Parts

Page Objects have a reference to the Page Parts that belong to them.

```
class HomePage(BasePage):
    def set_content(self, page):
        super().set_content(page)
        self.header = Header(self.page.locator(...))
```

When you need to do something in the page part, you can get the page part from
the parent.

```
def test_something(page):
    hp = HomePage(page)
    hp.navigate()
    hp.header.click_login_icon()
```

You shouldn't try to initialize a Page Part directly in your tests.

```
def test_something(page):
    hp = HomePage(page)
    hp.navigate()
    header = Header(hp.page.locator(...))  # Don't do this, use hp.header
    header.click_login_icon()
```

This pattern helps keep the code closer to how users think about
pages/page parts/actions. Users normally think like "Click the login icon in
the header of the home page", which translates to
`hp.header.click_login_icon()` in our syntax.

For the sake of simplicity, the Page Part objects have no reference to their
parents. So you can't do the following:

```
sidebar = header.parent.sidebar  # Page Parts have no parent attr storing a ref to parent
```

Rather, the parent has the reference to the child Page Part, and it is the
programmer's job to call the relevant page parts directly from their parents.

```
header = hp.header
# Do something with the header
header.click_login_icon()
sidebar = hp.sidebar  # Call another Page Part directly from the parent
# Do something with the sidebar
sidebar.select_language("en")
```

### Page Parts inside Page Parts

Complex pages can have complex page parts, which leads to the need for nesting
Page Parts. Luckily, due to Playwright's locator chaining, this is easy using
the `BasePagePart` class.

Let's say that the header's navigation menu is pretty complex, and we want to
represent the navigation menu's complexity in a separate class. We can do that
as follows.

```
class Header(BasePagePart):
    def __init__(self, page_part_locator):
        super().__init__(page_part_locator)
        # Initialize the navigation menu with a locator relative to this page part
        self.navigation_menu = NavigationMenu(self.page_part_locator.locator(...))

class NavigationMenu(BasePagePart):
    def __init__(self, page_part_locator):
        super().__init__(page_part_locator)

    def click_on_section_A():
        ...
```

Then, in our code, we can access the navigation menu as follows:

```
def test_something(page):
    hp = HomePage(page)
    hp.navigate()
    hp.header.navigation_menu.click_on_section_A()
```

This pattern prevents any class from getting bloated as the complexity can be
separated out into other Page Parts. It also encourages reusability, since a
page part may appear in multiple locations on the page
(more on how to do that later).

## Page Object and Page Part aware `expect()`

In tests, we may often want to test a certain property of a page or a page
part. In Playwright, this is done using the `expect()` method. For example,
to check that a page has an expected URL, you would do the following.

```
from playwright.sync_api import expect

def test_url(page):
    hp = HomePage(page)
    hp.navigate()
    # Here the .page is required as the vanilla expect() only takes Playwright objects as arg
    expect(hp.page).to_have_url(...)
```

To check that the header exists, you would do something like this

```
def test_header_exists(page):
    hp = HomePage(page)
    hp.navigate()
    # Here the .page_part_locator is used to pass a Playwright Locator object to expect()
    expect(hp.header.page_part_locator).to_be_visible()
```

From the point of view of readability, it would be better if we could pass
Page Objects and Page Parts directly to `expect()`.

For that reason, we define our own `expect()` method in `pages/base.py` which
works just like Playwright's `expect()`, but it also accepts Page Objects and
Page Parts as an argument.

```
from umspages.base import expect

def test_url(page):
    hp = HomePage(page)
    hp.navigate()
    expect(hp).to_have_url(...)

def test_header_exists(page):
    hp = HomePage(page)
    hp.navigate()
    expect(hp.header).to_be_visible()
```

If you follow the above rules, you should never have to access the attributes
`page_part_locator` of Page Parts or `page` of Page Objects directly in your
tests.

## Writing custom error messages

Since we are on the topic of assertions using `expect()`, it is to be noted
that at the time our test suite was first created, the Python version of Playwright
did not support custom error messages in the `expect()` function. However, this
feature is now [available](https://playwright.dev/python/docs/test-assertions#custom-expect-message).

For new page objects and tests, we recommend to include a custom
error message with your `expect()` calls as follows.

```
expect(header, "Header is not visible on homepage").to_be_visible()
```

Write the error message in such a way that a developer looking at the error
message can immediately get an idea of the following:

1. Where the error happened (e.g. on which page and page part) e.g.
   "*Notifications sidebar* is not visible after clicking bell icon on *home page (logged in)*"
2. Which expected condition was not fulfilled e.g.
   "Notifications sidebar *is not visible* after clicking bell icon on home page (logged in)"
3. Preceding actions, if relevant e.g.
   "Notifications sidebar is not visible *after clicking bell icon* on home page (logged in)"

## Inheritance patterns

### Superset pattern

#### Use case: When shared Page Part varies slightly across pages

Sometimes, a page part (like a navbar) may be shared across a few pages.
However, there are slight differences in how the page part appears in each page.

For example, in the Univention Portal, the navbar in the home page has a
notification icon, search icon and the hamburger icon on the right hand side.
The same navbar in the login page has only the hamburger icon.

In this situation, we recommend using a single class `Navbar` that contains a
superset of all elements and functionality of that page part across all pages.

```
class Navbar(BasePagePart):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.hamburger_icon = ...  # Login page has only this icon
        self.search_icon = ...  # Home page also has this icon
        self.notification_icon = ...  # Home page also has this icon
        ...

    def click_hamburger_icon():
        ...

    def click_search_icon():
        ...

    def click_notification_icon():
        ...
```

The reason that we don't represent the page specific complexities of the page
parts in our POM is because we don't get anything out of adding this complexity.

The developer has to keep track of this complexity anyway to write correct
tests. For example, the developer should never issue the command
`login_page.navbar.search_icon.click()` in a test anyway, since the login page
has no search icon, and such a test is doomed to fail. Therefore, we won't
save the developer any time or effort by somehow enforcing that
`login_page.navbar` has no `search_icon` attribute.

So it hardly matters that our `Navbar` class always has a `search_icon`
instance attribute even if the page holding a reference to it doesn't
actually have a search icon.

Also, from an error message perspective, there isn't much difference between
the message "LoginPageNavBar has no attribute 'search_icon'" and
"timeout waiting for 'search_icon'". At least not enough difference to
justify represent the page specific complexity in the POM.

### Simple inheritance

#### Use case 1: Representing common functionality in two page parts

Nevertheless, there are occasions when the superset (or flat) pattern won't
work. In such cases, it is also OK to use simple inheritance patterns.
For example, you can also do the following (but only if the superset pattern
is untenable for some reason).

```
class NotificationContainer(BasePagePart):
    """Common stuff goes here"""

class NotificationDrawer(NotificationContainer):
    """The notification drawer specific stuff"""

class PopupNotificationContainer(NotificationContainer):
    """Popup notification specific stuff"""
```

In the above example, we use simple inheritance because the notification
drawer and popup notification container are different page parts, but they
have many common functionality that are best put in one place
(which is the `NotificationContainer` in this case).

Using anything other than simple inheritance is not recommended. Please try to
avoid multiple inheritance or mixins. These patterns add too much complexity
and makes the code hard to understand. A bit of duplicated code is better than
that.

#### Use case 2: Different states of a page object e.g. logged in vs. logged out

Here, we are no longer talking about page parts, but rather full webpages. For
example, there could be two states of the home page: logged-in and logged-out.
We usually cannot use the superset pattern here because important methods
like `navigate()` would be different for the different states. Therefore, we
recommend the simple inheritance pattern yet again for this use case.

```
class HomePage(BasePage):
    """Common stuff goes here"""

class HomePageLoggedIn(HomePage):
    """Stuff specific to logged in state goes here"""

class HomePageLoggedOut(HomePage):
    """Stuff specific to logged out state goes here"""
```

#### Use case 3: Common stuff shared across all pages

Things like navbars etc. are shared across all pages. We can also use the
simple inheritance pattern to ensure that all pages have a reference to the
navbar.

```
class PortalPage(BasePage):
    def set_content(self, *args, **kwargs):
        super().set_content(*args, *kwargs)
        self.navbar = Navbar(self.page.locator(...))

class HomePage(PortalPage):
    """Common home page stuff goes here"""

class HomePageLoggedIn(HomePage):
    """Stuff specific to logged in state goes here"""

class HomePageLoggedOut(HomePage):
    """Stuff specific to logged out state goes here"""

class LoginPage(PortalPage):
    """Login page specific stuff goes here"""
```

Three main things to remember about representing complexity:

1. If you are trying to represent "on-off" type variations
   (i.e. differences arising from the binary presence or absence of elements
   or functionality), then use the superset pattern. For any other type of
   variation, use simple inheritance.

2. Don't use multiple inheritance or mixin patterns to represent
   complexity/variations. Or at least ask other developers before you do so.

3. The inheritance pattern in your code base will not be static. As the
   website grows (and changes), you will find that stuff that you thought were
   unique to a page is repeated elsewhere. So now you have to separate the
   common stuff out into a base class etc. This is normal and part of the job
   (to reduce duplicate code). Just try not to break existing interfaces while
   doing such refactoring.

## How we handle login states and navigation

There are two ways of handling login states of pages.

1. Page Objects may be login state unaware, which means the same PO is used
   to represent the logged-in and logged-out states of pages. This pattern
   uses conditional logic in their `navigate()` method to ensure that we
   reach the login state we need in testing.

    ```
    class ExamplePage(BasePage):
        def navigate(login=False):
            if login:
                # ensure logged-in state
            else:
                # ensure logged-out state
    ```

    Using this pattern leads to the login logic being present allover the POs,
    because many page actions may also be sensitive to login state.

2. The other way is to make Page Objects explicitly login-state aware.
   This means creating two POs e.g. `HomePageLoggedOut` and `HomePageLoggedIn`
   to capture the two login states of a page. This pattern avoids conditional
   login logic in POs.

We prefer the second explicit pattern.

### Navigation

Each page object has a `navigate()` method that represents the canonical way
to navigate to that page. POs representing logged out states have the
signature `navigate()`, while POs representing logged in states have the
signature `navigate(username, password)`.

The `navigate()` method is implemented in a recursive manner.

```
class UserSettingsPageLoggedIn(BasePage):
    def navigate(username, password):
        home_page = HomePageLoggedIn(username, password)
        home_page.navigate()  # Use navigate() from the previous page in the navigation path
        # Do something to navigate to User Settings Page from the Home Page
        home_page.reveal_sidebar()
        home_page.sidebar.click_user_settings()
```


If you trace back the navigation path, you will usually find a root page,
from which all navigation essentially starts
(this is the entry page of the web app). The root page's navigation method is
defined in absolute terms using a URL (and not defined in terms of any other
page's `navigate()` method). It is also responsible for ensuring a particular
login state.

```
class HomePageLoggedOut(HomePage):
    def navigate():
        self.logout()  # Ensures logged out state
        self.goto("/")  # Ensures a specific URL
```

The `navigate()` method of other pages do not worry about ensuring a
particular login states by defining their navigation with respect to another
PO that ensures the correct login state.

For this to work, we need two canonical root pages, one that ensures a
logged-in state and one that ensures a logged-out state.For example, we could
define the logged-in state of the home page (`HomePageLoggedIn`) as the
canonical root for logged in destinations. We could define the logged out
state of the home page (`HomePageLoggedOut`) as the canonical root for
logged out destinations. `HomePageLoggedIn` and `HomePageLoggedOut`'s
`navigate()` method are then the only methods in the entire POM that worries
about login states in their `navigate()` method. The rest of the POs are
free of login logic.

Consider the `navigate()` method of the `UserSettingsPageLoggedIn` again. By
defining its navigation with respect to `HomePageLoggedIn` it ensures that
the `navigate()` method will lead to the logged-in state of the page (as expected).

### Navigating to pages that open in a new tab

Navigating to certain pages from the root may be associated with opening new
tabs. In this case, we can make the page object aware of the new tab by calling
`set_content(new_tab)` inside the `navigate()` method. This will make `self.page`
point to the new tab and the page elements being defined with respect to the
new tab.

When the `navigate()` method opens new tabs, these tabs should be returned as
a tuple by the method.

Here's an example.

```
   class NextcloudAllFilesPage(NextcloudHomePage):
      def set_content(self, page: Page):
         super().set_content(page)
         self.new_file_folder = self.page.locator(...)
         ...

      def navigate(self, username: str, password: str):
         portal_home_page_logged_in = HomePageLoggedIn(self.page)    # Starts from previous page in navigation path
         portal_home_page_logged_in.navigate(username, password)
         portal_home_page_logged_in.is_displayed()
         nextcloud_tab = portal_home_page_logged_in.get_new_tab(
            portal_home_page_logged_in.files_tile
         )    # A new tab is opened during navigation
         nextcloud_tab.wait_for_url(re.compile("dir="))
         self.set_content(nextcloud_tab)    # The page object redefined self.page and elements wrt the new tab
         return nextcloud_tab    # Returns the new tab
```

## Assertions in POs

There are two camps when in comes to whether assertions should be put in POs.

1. The first camp advocates for not putting assertions in POs and putting all
   assertions in tests. This is to ensure that there is separation of concerns
   between POs and tests.

2. The other camp holds that assertions in POs is a good thing because it
   avoids code repetition.

Both sides have a point. But we need to make a choice so that we don't end up
using a mixture of the two patterns in the code base.

We decide for option 2 i.e. assertions can be put in POs, but with some
limitations. Here are the guidelines regarding that.

1. If you are implementing a simple and irreducible element interaction such
   as `click_login_button()`, and the end result of that action is not
   explicitly stated, then you shouldn't perform assertions to check the
   result of that action.

   In general, try to avoid writing such one-liner methods anyway, since these
   one-liners are better written directly in the tests.

    ```
    def click_login_button():
        self.login_button.click()
    ```

2. If you are implementation a method where the end result is explicitly
   stated in the method name and the end result is unambiguously clear, then
   you should perform an assertion at the end to check the result of that action

    ```
    def reveal_side_nav_drawer(self):  # Result is explicitly stated and unambiguously clear
        if self.side_nav_drawer.is_hidden():
            self.header.click_hamburger_icon()
        expect(self.side_nav_drawer).to_be_visible()  # Checks performed at end
    ```

3. If you are implementing a more complex method, composed of multiple steps
   to achieve a goal, e.g. `remove_all_notifications()`, then you should
   perform assertions to check that the intermediate results are correct.
   Basically, the method should complain exactly where a user will also
   complain if things are not going right in a multistep interaction.

    ```
    def remove_all_notifications(self):
        self.reveal_notification_drawer()
        count = self.notification_drawer.notifications.count()
        if self.notification_drawer.no_notifications_heading.is_visible():
            if count > 0:
                raise PortalError("'No notifications' visible even when non-zero notifications present")  # check
            else:
                self.hide_notification_drawer()
        elif count == 1:
            self.notification_drawer.notification(0).click_close_button()
            expect(self.notification_drawer).to_be_hidden()  # check intermediate result
        else:
            self.notification_drawer.click_remove_all_button()
            expect(self.notification_drawer).to_be_hidden()  # check intermediate result
        self.reveal_notification_drawer()
        expect(self.notification_drawer.no_notifications_heading).to_be_visible()  # check final results
        expect(self.notification_drawer.notifications).to_have_count(0)  # check final results
        self.hide_notification_drawer()
    ```
