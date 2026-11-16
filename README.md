# LaTeX-viitteiden-hallinta

## Dokumentaatio

- [Pelisäännöt](docs/pelisaannot.md)
- [Backlogit](https://github.com/users/source-exp/projects/1)
- [Lisenssi](LICENSE)
## Definition of Done

User story on valmis, kun kaikki seuraavat ehdot täyttyvät:

- Storylle on kirjattu selkeät hyväksymiskriteerit.
- Hyväksymiskriteerit täyttyvät toteutuksessa ja ne on testattu tarkoituksenmukaisesti. Sprintistä 2 alkaen hyväksymiskriteerit kirjataan Robot Framework -testeinä.
- Toteutuksella on kohtuullinen testikattavuus, ja testit menevät läpi jatkuvan integraation (CI) yhteydessä.
- Koodi on luettavaa ja ylläpidettävää: nimeäminen, rakenne ja arkkitehtuuri ovat selkeitä ja projektin koodityyliä noudatetaan.
- Tarvittavat Pylint-tarkistukset menevät läpi.
- Toteutus on integroitu `main`-haaraan ja asiakas voi tarkistaa koodin ja testien tilanteen CI-palvelusta.
- Story toimii OKD-klusterilla olevassa sovellusversiossa.
- Toteutus, testit ja tarvittavat dokumentaation tai konfiguraation muutokset ovat mukana GitHub-repositoriossa.

- [CI / GitHub Actions](https://github.com/source-exp/LaTeX-viitteiden-hallinta/actions)
- [OKD-sovellus](https://route-ohjelmistotuotanto-lahiopetus-2026-7.ext.okd-cs-test-0.k8s.cs.helsinki.fi)

OKD-deploymentin käyttöönotto on kuvattu tiedostossa
[`kustomization.yaml`](kustomization.yaml). Ennen ensimmäistä deployausta
luo `secret.env`
mallista `secret.env.template` ja suorita:

```sh
oc project <namespace>
oc apply -k .
oc rollout status deploy/dep
oc exec deploy/dep -- python src/db_helper.py
```
