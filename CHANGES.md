
<a name="v2.4.0"></a>
## [v2.4.0](https://github.com/jasondelaat/pymonad/compare/v2.3.5...v2.4.0) (2021-05-14)

### Feat

* Adds function pymonad.tools.monad_from_none_or_value


<a name="v2.3.5"></a>
## [v2.3.5](https://github.com/jasondelaat/pymonad/compare/v2.3.4...v2.3.5) (2021-04-15)

### Chore

* Updates README with note about performance issues prior to 2.3.4

### Fix

* Fixes implementations of bind(), map(), and then() for Promise monad
* Fixes implementations of amap(), bind(), map(), and then() for State monad
* Fixes implementation of then() for the ListMonad
* Fixes implementation of then() for the Reader monad
* Fixes implementation of then() for the IO monad
* Fixes default implementation of then() to be more efficient
* Fixes join() methods so it raises a TypeError if monad instance is not nested


<a name="v2.3.4"></a>
## [v2.3.4](https://github.com/jasondelaat/pymonad/compare/v2.3.3...v2.3.4) (2021-03-07)

### Chore

* Updates .gitignore

### Fix

* Fixes a bunch of pytype errors
* Changes Either so it no longer automatically catches exceptions in a Left constructor


<a name="v2.3.3"></a>
## [v2.3.3](https://github.com/jasondelaat/pymonad/compare/v2.3.2...v2.3.3) (2021-02-01)


<a name="v2.3.2"></a>
## [v2.3.2](https://github.com/jasondelaat/pymonad/compare/v2.3.1...v2.3.2) (2021-01-14)


<a name="v2.3.1"></a>
## [v2.3.1](https://github.com/jasondelaat/pymonad/compare/v2.3.0...v2.3.1) (2021-01-03)


<a name="v2.3.0"></a>
## [v2.3.0](https://github.com/jasondelaat/pymonad/compare/v2.2.0...v2.3.0) (2020-11-25)


<a name="v2.2.0"></a>
## [v2.2.0](https://github.com/jasondelaat/pymonad/compare/v2.1.0...v2.2.0) (2020-10-01)


<a name="v2.1.0"></a>
## [v2.1.0](https://github.com/jasondelaat/pymonad/compare/v2.0.5...v2.1.0) (2020-09-22)


<a name="v2.0.5"></a>
## [v2.0.5](https://github.com/jasondelaat/pymonad/compare/v2.0.4...v2.0.5) (2020-09-22)


<a name="v2.0.4"></a>
## [v2.0.4](https://github.com/jasondelaat/pymonad/compare/v2.0.3...v2.0.4) (2020-08-03)


<a name="v2.0.3"></a>
## [v2.0.3](https://github.com/jasondelaat/pymonad/compare/v2.0.2...v2.0.3) (2020-08-03)


<a name="v2.0.2"></a>
## [v2.0.2](https://github.com/jasondelaat/pymonad/compare/v2.0.1...v2.0.2) (2020-08-03)


<a name="v2.0.1"></a>
## [v2.0.1](https://github.com/jasondelaat/pymonad/compare/v2.0.0...v2.0.1) (2020-08-02)


<a name="v2.0.0"></a>
## [v2.0.0](https://github.com/jasondelaat/pymonad/compare/v1.3...v2.0.0) (2020-07-14)

### Reverts

* Renamed Monad.fmap to Monad.map.


<a name="v1.3"></a>
## [v1.3](https://github.com/jasondelaat/pymonad/compare/v1.2...v1.3) (2014-06-28)


<a name="v1.2"></a>
## [v1.2](https://github.com/jasondelaat/pymonad/compare/v1.1...v1.2) (2014-05-17)


<a name="v1.1"></a>
## [v1.1](https://github.com/jasondelaat/pymonad/compare/v1.0...v1.1) (2014-04-13)


<a name="v1.0"></a>
## v1.0 (2014-03-29)

