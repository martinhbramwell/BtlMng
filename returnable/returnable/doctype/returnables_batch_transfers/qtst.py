#!/usr/bin/env python3

testData = [
    {
        "customer": "Yael Esmeralda Cerda Verdesoto",
        "serial_nos": [
            "IBAA032",
            "IBAA035",
            "IBAA120"
        ]
    },
    {
        "customer": "Julien Reynaud",
        "serial_nos": [
            "IBAA443",
            "IBAA503",
            "IBAA504"
        ]
    },
    {
        "customer": "Luis Eduardo Cordovez",
        "serial_nos": [
            "IBAA149",
            "IBAA251",
            "IBAA272"
        ]
    },
    {
        "customer": "Maria Correa",
        "serial_nos": [
            "IBAA009",
            "IBAA642"
        ]
    },
    {
        "customer": "Abner Victor Manuel Galarza Sosa",
        "serial_nos": [
            "IBAA022",
            "IBAA342",
            "IBAA348"
        ]
    },
    {
        "customer": "Acrimecsa del Ecuador S.A",
        "serial_nos": [
            "IBAA339",
            "IBAA370",
            "IBAA629"
        ]
    }
]

def orderBySerialNumber(customerSerialNumbers):
  customerOfSerialNumber = []
  for customer in customerSerialNumbers:
    customerName = customer["customer"]
    # print(customerName)
    for serialNumber in customer["serial_nos"]:
      # print(serialNumber)
      customerOfSerialNumber.append({ "serialNumber": serialNumber, "customer": customerName })

  print(customerOfSerialNumber[0])
  customerOfSerialNumber.sort(key=lambda entry: entry["serialNumber"])
  return customerOfSerialNumber




def main():
  customerOfSerialNumber = orderBySerialNumber(testData)
  print(customerOfSerialNumber[0])


if __name__ == '__main__':
  main()
  print("-------")

