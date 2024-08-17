# Page Object Model Inheritance Patterns

## Superset pattern

### Use case: When shared Page Part varies slightly across pages

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

## Simple inheritance

### Use case 1: Representing common functionality in two page parts

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

### Use case 2: Different states of a page object e.g. logged in vs. logged out

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

### Use case 3: Common stuff shared across all pages

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
